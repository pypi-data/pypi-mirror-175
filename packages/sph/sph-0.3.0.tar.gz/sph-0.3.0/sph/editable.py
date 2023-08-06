import ast
import re
from concurrent.futures import ThreadPoolExecutor

from git.repo import Repo

from sph.conan_ref import ConanRef

def create_editable_dependency(editable, editables):
    all_required_lib = []
    with open(editable.conan_path, "r") as conanfile:
        conanfile_ast = ast.parse(conanfile.read())
        for node in ast.iter_child_nodes(conanfile_ast):
            if isinstance(node, ast.ClassDef):
                for class_node in ast.iter_child_nodes(node):
                    if isinstance(class_node, ast.Assign):
                        for target in class_node.targets:
                            if target.id == "requires":
                                all_required_lib += [
                                    elt.value for elt in class_node.value.elts
                                ]

        for dep in all_required_lib:
            dep_name = dep.split("/")[0]
            if dep_name != editable.package.name:
                if dep_name in [x.package.name for x in editables]:
                    dep_editable = next(x for x in editables if x.package.name == dep_name)
                    if dep_editable is not None:
                        editable.required_local_lib.append(ConanRef(dep))
                else:
                    editable.required_external_lib.append(
                        ConanRef(dep)
                    )


def create_editable_from_workspace(workspace, github_client=None, thread_pool=None):
    editable_list = []

    for conan_ref, project_conan_path in workspace.local_refs:
        if project_conan_path.exists():
            conan_ref.is_present_locally = True
            editable_list.append(Editable(conan_ref.package, project_conan_path, github_client, thread_pool))
        else:
            conan_ref.is_present_locally = False

    for ed in editable_list:
        create_editable_dependency(ed, editable_list)

    return editable_list

class Editable:
    def __init__(self, conan_package, conan_path, gh_client, thread_pool):
        self.thread_pool = thread_pool
        self.package = conan_package
        self.conan_path = conan_path / "conanfile.py" if "conanfile.py" not in str(conan_path) else conan_path
        self.repo = Repo(self.conan_path.parents[1].resolve())
        self.required_external_lib = []
        self.required_local_lib = []
        self.gh_repo_name = None
        self.gh_repo = None
        self.future = None
        self.current_run = None
        self.runs_develop = []

        remote_url = list(self.repo.remote("origin").urls)[0]
        match = re.search(r"github.com:(.*)/(.*(?=\.g)|.*)", remote_url)

        if match and gh_client:
            self.org = match.group(1)
            self.gh_repo_name = match.group(2)
            self.gh_client = gh_client

        self.setup_gh_repo()

    def change_version(self, new_dependency, old_dependency=None):
        text = None
        regex = r''
        if old_dependency is None:
            regex = r"{}\/[\w]+@[\w]+\/[\w]+(#[\w])?".format(re.escape(new_dependency.package.name))
        else:
            regex = re.escape(old_dependency)

        with open(self.conan_path, "r") as conanfile:
            text = conanfile.read()
            text = re.sub(regex, new_dependency.ref, text)
        with open(self.conan_path, "w") as resolvedfile:
            resolvedfile.write(text)

        for dep in self.required_local_lib:
            if dep.package.name == new_dependency.package.name:
                dep.version = new_dependency.version
                dep.user = new_dependency.user
                dep.channel = new_dependency.channel
                dep.revision = new_dependency.revision

        for dep in self.required_external_lib:
            if dep.package.name == new_dependency.package.name:
                dep.version = new_dependency.version
                dep.user = new_dependency.user
                dep.channel = new_dependency.channel
                dep.revision = new_dependency.revision


    def setup_gh_repo_task(self):
        if self.gh_repo:
            return True

        try:
            self.gh_repo = self.gh_client.get_repo(f"{self.org}/{self.gh_repo_name}")
            return True
        except Exception:
            self.gh_repo = False
            return False
        
    def setup_gh_repo(self):
        if self.gh_repo_name:
            f = self.thread_pool.submit(self.setup_gh_repo_task)
            f.add_done_callback(self.check_workflow)
    
    def get_dependency_from_package(self, package):
       return next(filter(lambda x: x.package == package, self.required_external_lib + self.required_local_lib))

    def checking_workflow_task(self, force=False):
        if self.current_run and not force:
            return self.current_run

        try:
            runs_queued = self.gh_repo.get_workflow_runs(
                branch=self.repo.active_branch.name, status='queued'
            )
            runs_in_progress = self.gh_repo.get_workflow_runs(
                branch=self.repo.active_branch.name, status='in_progress'
            )
            runs_completed = self.gh_repo.get_workflow_runs(
                branch=self.repo.active_branch.name, status='completed'
            )
            self.runs_develop = self.gh_repo.get_workflow_runs(
                branch="develop", status="completed"
            )
            if (
                runs_queued.totalCount > 0
                or runs_in_progress.totalCount > 0 or runs_completed.totalCount > 0
            ):
                for run in (
                        list(runs_queued)
                        + list(runs_in_progress) + list(runs_completed)
                ):
                    if run.head_sha == self.repo.head.commit.hexsha:
                        self.current_run = run

            if self.current_run:
                return self.current_run
            else:
                self.current_run = False
        except Exception:
            self.current_run = False

    def check_workflow(self, f):
        if self.gh_repo:
            exe = ThreadPoolExecutor(max_workers=1)
            exe.submit(self.checking_workflow_task)
