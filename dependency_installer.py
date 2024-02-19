import os
import sys
import tempfile
import subprocess
import colorprint.colorprint
import git_api.api_git
import pwd
import inquirer

class DependencyWalker():

    dependencywalker_dependencies = ["git", "curl", "ca-certificates", "apt-transport-https", "lsb-release","gnupg", "gnupg2", "software-properties-common"]
    
    stacks = [
        "ALL",
        "NodeJs",
        "NPM",
        "NVM - Node Version Manager",
        "PHP",
        "Composer - PHP Dependency Manager",
        "Rbenv - Ruby Version Manager",
        "Docker",
        "Docker-Compose"
    ]

    install_choices = [
        inquirer.Checkbox(
            name="Tech",
            message="Select the software you want to install",
            choices=stacks
        )
    ]

    temp_dir = tempfile.mkdtemp()

    hardcoded_docker_compose_version = "v2.24.6"

    hardcoded_nvm_version = "v0.39.7"

    def install(self):
        colorprint.print_success("[+] Starting Installations")
        stacks = inquirer.prompt(self.install_choices)
        if 'ALL' in stacks['Tech']:
            colorprint.print_success("[+] You Have Selected ALL Option")
            colorprint.print_success("[+] Installing FULL-PACKAGES")
            self.install_all_stack()
            return
        
        for stack in stacks["Tech"]:
            match stack:
                case 'NodeJs':
                    self.install_nodejs()
                    continue
                case 'NPM':
                    self.install_npm()
                    continue
                case 'NVM - Node Version Manager':
                    self.install_nvm()
                    continue
                case 'PHP':
                    self.install_php()
                    continue
                case 'Composer - PHP Dependency Manager':
                    self.install_php_compose()
                    continue
                case 'Rbenv - Ruby Version Manager':
                    self.install_rbenv()
                    continue
                case 'Docker':
                    self.install_docker()
                    continue
                case 'Docker-Compose':
                    self.install_docker_compose()
                    continue
                case _:
                    colorprint.print_error(f" [!] Invalid Option Selected - {stack}")
                    continue
            
        if ('NodeJs' in stacks["Tech"] or 'NPM' in stacks["Tech"]) and 'NVM - Node Version Manager' in stacks["Tech"]:
            colorprint.print_success(" [+] ATTETION: If you are a more experienced developer, install Node.JS/NPM again using NVM, the Node.js/NPM installed by this script may not be in the latest version.")

        if 'Rbenv - Ruby Version Manager' in stacks["Tech"]:
            colorprint.print_success(" [+] ATTETION: Ruby was not installed, you need to run the 'rbenv install -l' command to install it in your environment.")

    def install_all_stack(self):
        self.install_nodejs()
        self.install_npm()
        self.install_nvm()
        self.install_php()
        self.install_php_compose()
        self.install_rbenv()
        self.install_docker()
        self.install_docker_compose()

    def __is_package_installed__(self, package_name) -> bool:
        try:
            subprocess.check_call(['dpkg-query', '-W', '-f=${Status}', package_name], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return True
        except:
            return False
        
    def __install_apt_package__(self, package_name) -> bool:
        return os.system(f"sudo apt-get install -y {package_name}") == 0
    
    def __update_repositories__(self):
        return os.system("sudo apt-get update -y") == 0

    def __update_packages__(self):
        return os.system("sudo apt-get upgrade -y") == 0

    def __check_packages_and_install__(self):
        print(" [+] Updating Repositories")
        if self.__update_repositories__() is False:
            colorprint.print_error(" [!] Failed To Update Repositories, Ignoring..")
        else:
            colorprint.print_success(" [+] Repositorires Updated")
        
        if self.__update_packages__() is False:
            colorprint.print_error(" [!] Failed To Update Installed Packages, Ignoring..")
        else:
            colorprint.print_success(" [+] Installed Packages Updated Sucessfully")

        for depedency in self.dependencywalker_dependencies:
            # we need to FORCE git installation.
            if depedency == "git":
                print(" [+] Installing Git")
                os.system("sudo apt install git -y")
                os.system("clear")
            print(f" [+] Checking {depedency}")
            if self.__is_package_installed__(depedency) is False:
                colorprint.print_error(f" [!] {depedency} Is Not Installed")
                print(f" [!] Installing {depedency}")
                if self.__install_apt_package__(depedency) is False:
                    colorprint.print_error(f" [!] Failed To Install {depedency}, please install {depedency} manually, then, run the py script again")
                    sys.exit(-1);
                else:
                    colorprint.print_success(f" [+] {depedency} Installed Sucessfully")
            else:
                colorprint.print_success(f" [+] {depedency} - OK")
        
    def __init__(self):
        print("[+] Checking DependencyInstaller Dependencies")
        self.__check_packages_and_install__()
    
    def __download_file__(self, url, file_name) -> str:
        path = f"{self.temp_dir}/{file_name}";
        cmd = f"wget -c -O {path} {url}";
        os.system(cmd);
        return path;
      
    def install_nodejs(self):
        colorprint.print_success("[+] Installing !NodeJs!")        
        ret_code = os.system("curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg")
        if ret_code is not 0:
            colorprint.print_error(" [!] FAILED TO GET 'nodesource.gpg'")
            sys.exit(-1)
        else:
            colorprint.print_success(" [+] nodesource.gpg Downloaded Sucessfully")

        os.system("NODE_MAJOR=20")
        os.system('echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list') 
        if self.__install_apt_package__('nodejs') is False:
            colorprint.print_error(" [!] FAILED TO INSTALL NodeJs | Ignoring.")
            return
        colorprint.print_success(" [+] NodeJS Installed Sucessfully")

    def install_npm(self):
        colorprint.print_success("[+] Installing !npm!")
        ret_code = os.system("sudo apt-get install -y npm")
        if ret_code is not 0:
            colorprint.print_error(f" [!] NPM Installation Failure")
            return
        colorprint.print_success(" [+] NPM Installation Success")
        return
    
    def install_nvm(self):
        colorprint.print_success("[+] Installing !NVM!")
        colorprint.print_success(" [+] Getting Latest NVM Version")
        latest_nvm_version = git_api.get_repo_last_tag_version("nvm-sh", "nvm")
        if latest_nvm_version is None:
            colorprint.print_error(" [!] Failed To Get Latest NVM Version")
            colorprint.print_error(f"  [!] Selecting HardCoded NVM Version [{self.hardcoded_nvm_version}]")
            nvm_script_url = f"https://raw.githubusercontent.com/nvm-sh/nvm/{self.hardcoded_nvm_version}/install.sh"
        else:
            colorprint.print_success(" [+] Success In Obtaining Last NVM Version")
            colorprint.print_success(f"    [+] Last NVM Version - {latest_nvm_version}")
            nvm_script_url = f"https://raw.githubusercontent.com/nvm-sh/nvm/{latest_nvm_version}/install.sh"
        colorprint.print_success(" [+] Downloading NVM Bash Script")
        ret_code = os.system(f"curl -o- {nvm_script_url} | bash")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Install NVM | IGNORING NVM")
            return
        colorprint.print_success(" [+] NVM Installation Success")

    def install_docker(self):
        colorprint.print_success("[+] Installing !Docker!")
        colorprint.print_success(" [+] Preparing Environment/APT Repos to Docker")
        ret_code = os.system("sudo install -m 0755 -d /etc/apt/keyrings")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Create keyrings dir | IGNORING DOCKER")
            return
        ret_code = os.system("sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Fetch docker gpg key [docker.asc] | IGNORING DOCKER")
            return
        ret_code = os.system("sudo chmod a+r /etc/apt/keyrings/docker.asc")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Give Read Permissions to '/etc/apt/keyrings/docker.asc' file | IGNORING DOCKER")
            return
        

        docker_cmd_sh_file = "shell_scripts/docker_env.sh"
        if os.path.exists(docker_cmd_sh_file) is False:
            colorprint.print_error(" [!] Failed To Run 'docker_env.sh' file, IGNORING DOCKER INSTALLATION")
            return

        colorprint.print_success(" [+] Giving docker_env.sh 'Execute' Permissions")
        perm_ret = subprocess.run(['sudo', 'chmod', '+x', docker_cmd_sh_file])
        if perm_ret.returncode is not 0:
            colorprint.print_error(f" [!] Failed To Give 'Execute' permissions to {docker_cmd_sh_file} file, ERROR: {perm_ret.stderr} | IGNORING DOCKER")
            return

        result = subprocess.run([docker_cmd_sh_file], shell=True, capture_output=True, text=True)
        if result.returncode is not 0:
            colorprint.print_error(f" [!] Failed To Prepare Sys Environment To Docker Installation | ERROR: {result.stderr}")
            return
        
        colorprint.print_success(" [+] Updating Repositories")
        if self.__update_repositories__() is False:
            colorprint.print_error(" [!] Failed To Update Repos, this can make the docker installation fails")
        else:
            colorprint.print_success(" [+] Repositories Update Success")
        colorprint.print_success(" [+] Updating Packages")
        if self.__update_packages__() is False:
            colorprint.print_error(" [!] Failed To Update Packages, this can make the docker installation fails")
        else:
            colorprint.print_success(" [+] Packages Update Success")
        


        ret_code = os.system("sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Install Docker | IGNORING DOCKER")
            return
        colorprint.print_success(" [+] Docker Installation Success")
    
        uid = os.getuid()
        colorprint.print_success(" [+] Adding user to docker group")
        user_1 = os.getlogin()
        user_2 = pwd.getpwuid(uid).pw_name
        ret_code = os.system(f"sudo usermod -aG docker {user_1}")
        if ret_code is not 0:
            colorprint.print_error(f" [!] Failed To ADD {user_1} to docker group | Trying with {user_2}")
        ret_code = os.system(f"sudo usermod -aG docker {user_2}")
        if ret_code is not 0:
            colorprint.print_error(f" [!] Failed To ADD {user_2} to docker group, you need to add yourself")
            return
    
    def install_docker_compose(self):
        docker_compose_file_path = "/usr/local/bin/docker-compose"


        colorprint.print_success("[+] Installing !docker-compose!")
        colorprint.print_success(" [+] Getting Latest Docker-Compose Version")
        latest_docker_compose_version = git_api.get_repo_last_tag_version("docker", "compose")
        sys_name = os.uname().sysname
        sys_arch = os.uname().machine
        if latest_docker_compose_version is None:
            colorprint.print_error(" [!] Failure Getting Latest Docker-Compose Version")
            colorprint.print_error(f" [!] Selecting HardCoded Docker-Compose Version [{self.hardcoded_docker_compose_version}]")
            docker_compose_repo_url = f"https://github.com/docker/compose/releases/download/{self.hardcoded_docker_compose_version}/docker-compose-{sys_name}-{sys_arch}"
        else:
            colorprint.print_success(" [+] Success Getting Latest Docker-Compose Version")
            colorprint.print_success(f" [+] Last Docker-Compose Version - {latest_docker_compose_version}")
            docker_compose_repo_url = f"https://github.com/docker/compose/releases/download/{latest_docker_compose_version}/docker-compose-{sys_name}-{sys_arch}"

        ret_code = os.system(f"sudo curl -L {docker_compose_repo_url} -o {docker_compose_file_path}")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failure Downloading Docker-Compose Repository | Ignoring")
            return
        colorprint.print_success(" [+] Success Downloading Docker-Compose Repository")
        colorprint.print_success(" [+] Giving Docker-Compose Execution Permissions")
        ret_code = os.system(f"sudo chmod +x {docker_compose_file_path}")
        if ret_code is not 0:
            colorprint.print_error(f" [!] Failure Giving Execute Permissions To Docker-Compose | command: 'sudo chmod +x {docker_compose_file_path}'")
        colorprint.print_success(" [+] Added execution permissions to docker-compose with success")
        colorprint.print_success(" [+] Adding docker-compose symbolic link")
        ret_code = os.system(f"sudo ln -s {docker_compose_file_path} /usr/bin/docker-compose")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failure Adding docker-compose symbolic link")
            colorprint.print_error(f" [!] This is not a serious error, however, it could cause problems in the future, as whenever you reference docker-compose, it will need to be through its absolute path, e.g.: {docker_compose_file_path} up")
        colorprint.print_success(" [+] Docker-Compose Installation Sucessfully!")
        colorprint.print_success(f" [+] You Can Call Docker-Compose with '{docker_compose_file_path} up' or 'docker-compose up'")
        return

    def install_php(self):
        colorprint.print_success("[+] Installing !PHP! + !PHP-Extensions!")
        colorprint.print_success(" [+] Installing PHP")
        ret_code = os.system("sudo apt install -y php")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Install PHP | IGNORING PHP")
            return
        
        colorprint.print_success(" [+] Installing PHP Extensions")
        ret_code = os.system("sudo apt install -y libapache2-mod-php php-pdo php-mysql php-curl php-gd php-pear php-imagick php-imap php-memcache php-pspell php-snmp php-tidy php-xmlrpc php-xsl php-zip")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Install PHP Extensions | IGNORING PHP EXTENSIONS")
            return

        colorprint.print_success(" [+] PHP && PHP Extensions Installed Sucessfully")

    def install_php_compose(self):
        colorprint.print_success("[+] Installing !Composer! - PHP Depedency Manager")
        composer_temp_path = f"{self.temp_dir}/composer-setup.php"
        composer_install_dir = "/usr/local/bin"

        colorprint.print_success(" [+] Downloading composer.php")
        ret_code = os.system(f"wget https://getcomposer.org/installer -O {composer_temp_path}")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Download Composer | IGNORING COMPOSER")
            return
        ret_code = os.system(f"sudo php {composer_temp_path} --install-dir={composer_install_dir} --filename=composer")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Install Composer | IGNORING COMPOSER")
            return
        colorprint.print_success(" [+] Composer Has Been Installed Successfully")

    def install_rbenv(self):
        colorprint.print_success("[+] Installing !rbenv!")
        ret_code = os.system("git clone https://github.com/rbenv/rbenv.git ~/.rbenv")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Clone rbenv repository | IGNORING RBENV")
            return
        colorprint.print_success(" [+] rbenv repo downloaded sucessfully")
        colorprint.print_success(" [+] Loading rbenv in shell")
        ret_code = os.system("echo 'eval \"$(~/.rbenv/bin/rbenv init - bash)\"' >> ~/.bashrc")
        if ret_code is not 0:
            colorprint.print_error(" [!] Failed To Load rbenv in shell profile - '~/.bashrc' | IGNORING RBENV")
            return
        colorprint.print_success(" [+] rbenv installed sucessfully")

os.system("clear")
print(" [+] Dependency Installer Py Script [+]")
print(" [+] Author: LeandroVictor666 [+]")
print("\n")
colorprint.print_success("[+] Initializing Tool..")
dw = DependencyWalker()
dw.install()
