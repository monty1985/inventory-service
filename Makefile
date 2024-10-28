VENV_PATH = ./.venv

.PHONY: create-venv
create-venv:
	@python3 scripts/dependency_manager.py create-venv

.PHONY: install-dependencies
install-dependencies:
	@python3 scripts/dependency_manager.py install

.PHONY: add-dependency
add-dependency:
	@read -p "Enter dependency name: " dep; \
	python3 scripts/dependency_manager.py add $$dep

.PHONY: list-dependencies
list-dependencies:
	@python3 scripts/dependency_manager.py list
