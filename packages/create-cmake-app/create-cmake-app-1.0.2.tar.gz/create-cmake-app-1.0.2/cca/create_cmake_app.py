import os
import sys
import argparse
import textwrap
import subprocess

from pathlib import Path


def log_status(func):
    def wrapper(path, content):
        print(f"Creating {str(path)}...")
        func(path, content)
        print(f"Done creating {str(path)}", end="\n\n")

    return wrapper


def write_to_output(path, content):
    with open(path, "wt", encoding="utf-8") as output:
        output.write(textwrap.dedent(content))


@log_status
def create_nested_file(path, content):
    path.touch()
    write_to_output(path, content)


def main():
    parser = argparse.ArgumentParser(
        description="create cmake app cli tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            navigate to destination and run:
            python main.py -n <your-project-name> (REQUIRED) # if you run script directly
            cca -n <your-project-name> (REQUIRED)

            script will generate project directory and necessary nested template files
                               """
        ),
    )
    parser.add_argument("-n", "--name", help="project name")
    parser.add_argument(
        "-em",
        "--external-mode",
        help="how external libararies should be added; e.g. submodule, fetchcontent",
    )

    args = parser.parse_args()

    if not args.name:
        print("Please provide project directory name!")
        sys.exit(1)

    if not args.external_mode:
        print(
            "Please choose how external libraries should be added (git submodule add, FetchContent)"
        )
        sys.exit(1)

    project_name = args.name
    cwd = Path(os.getcwd())
    # create project directory
    print(f"creating project directory: {project_name}...")
    os.mkdir(cwd.joinpath(project_name))

    project_dir_path = Path(cwd.joinpath(project_name))
    cmake_dir_path = Path(project_dir_path.joinpath("cmake"))
    app_dir_path = Path(project_dir_path.joinpath("app"))
    src_dir_path = Path(project_dir_path.joinpath("src"))
    src_include_dir_path = Path(src_dir_path.joinpath("include"))
    external_dir_path = Path(project_dir_path.joinpath("external"))

    # put in here for nested directories creation
    nested_dirs = [
        cmake_dir_path,
        app_dir_path,
        src_dir_path,
        src_include_dir_path,
    ]
    if args.external_mode == "submodule":
        nested_dirs.append(external_dir_path)

    # creating directories
    for dir in nested_dirs:
        dir.mkdir()
        print(f"{str(dir)} created")

    # root Makefile
    create_nested_file(
        Path(project_dir_path.joinpath("Makefile")),
        """\
            exe_name := task

            all: run

            clean:
	        \tif [ -d ./build/_deps ]; then mv ./build/_deps ./; fi
	        \trm -rf ./build
	        \tmkdir build
	        \tif [ -d ./_deps ]; then mv ./_deps ./build; fi

            build: clean
            \tcmake -S . -B ./build -GNinja
            \tif [ -d ./build/app ]; then cmake --build ./build --target $(exe_name); \
            \telse cmake --build ./build; fi
            \tmv ./build/compile_commands.json .

            run: build
            \t./build/app/Debug/$(exe_name).exe
        """,
    )

    # root CMakeLists.txt
    s = ""
    s += textwrap.dedent(
        """\
        cmake_minimum_required(VERSION 3.21)

        project(task)

        set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
        set(CMAKE_CXX_STANDARD 17)
        set(CMAKE_CXX_STANDARD_REQUIRED ON)
        set(CMAKE_CXX_EXTENSIONS OFF) 

    """
    )

    if args.external_mode == "submodule":
        s += textwrap.dedent(
            """\
            set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/")
            include(AddGitSubmodule)

        """
        )

    else:
        s += textwrap.dedent(
            """\
            # uncomment below and add desired libararies
            include(FetchContent)
            # FetchContent_Declare(
            #     SFML
            #     GIT_REPOSITORY https://github.com/SFML/SFML.git
            #     GIT_TAG 2.6.x
            # )
            # FetchContent_MakeAvailable(SFML)

        """
        )

    s += textwrap.dedent(
        """
        add_subdirectory(src)
        add_subdirectory(app)
    """
    )

    create_nested_file(Path(project_dir_path).joinpath("CMakeLists.txt"), s)

    # AddGitSubmodule.cmake
    if args.external_mode == "submodule":
        create_nested_file(
            Path(cmake_dir_path).joinpath("AddGitSubmodule.cmake"),
            """\
                function(add_git_submodule dir)
                \tfind_package(Git REQUIRED)

                \tif (NOT EXISTS ${dir}/CMakeLists.txt)
                \t\texecute_process(COMMAND ${GIT_EXECUTABLE}
                \t\t\tsubmodule update --init --recursive -- ${dir}
                \t\t\tWORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
                \tendif()

                \tadd_subdirectory(${dir})
                endfunction() 
            """,
        )

    # app/main.cpp
    create_nested_file(
        Path(app_dir_path).joinpath("main.cpp"),
        """\
            #include <iostream>

            int main() {
                std::cout << "hello from create cmake app!" << '\\n';
                return 0;
            }
        """,
    )

    # app/CMakeLists.txt
    create_nested_file(
        Path(app_dir_path).joinpath("CMakeLists.txt"),
        """\
            set(EXECUTABLE_SOURCES 
                "main.cpp")

            add_executable(${PROJECT_NAME} ${EXECUTABLE_SOURCES})
        """,
    )

    # src/CMakeLists.txt
    # src/include/CMakeLists.txt
    # empty CMakeLists.txt, add custom later
    Path(src_dir_path).joinpath("CMakeLists.txt").touch()
    print("Done creating src/CMakeLists.txt\n")

    # .gitignore
    create_nested_file(
        Path(project_dir_path).joinpath(".gitignore"),
        """\
            .ccls-cache/
            external/
            build/
            compile_commands.json
        """,
    )

    # git init
    os.chdir(project_dir_path)
    result = subprocess.run(["git", "init"], stdout=subprocess.PIPE)
    print(result, end="\n\n")

    print("Done generating cmake template project!")


if __name__ == "__main__":
    main()
