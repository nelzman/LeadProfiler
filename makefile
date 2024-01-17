python_local_environment_name := local_dev
make_file_path := $(abspath $(lastword $(MAKEFILE_LIST)))
cwd := $(dir $(make_file_path))

new_environment:
	conda env create --file infrastructure/environment.yml

update_environment:
	conda env update --name lead_profiler --file environment.yml

export_environment:
	conda env export --name lead_profiler > environment.yml

remove_environment:
	conda env remove --name lead_profiler

start_app: 
	python -m lead_profiler_app

