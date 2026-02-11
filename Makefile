### Test and build your Lambda in a given Node environment and release your new build via Cosmos.

### Variables ###
NODE_VERSION ?= 20
COMPONENT_NAME ?= your-component-name
CERT ?= ~/.certee/client.crt
KEY ?= ~/.certee/client.key
PROJECT_PATH ?= Developer    

CONTAINER := $(shell command -v podman || command -v docker)
WITH_CONTAINER := $(CONTAINER) run \
	-v "$$(pwd)/..":/workspace:rw \
	-v $(CERT):/etc/pki/tls/certs/client.crt \
    -v $(KEY):/etc/pki/tls/private/client.key \
	-w "/workspace/$$(basename $$(pwd))" \
	--rm \
	470820891875.dkr.ecr.eu-west-1.amazonaws.com/bbc-el9-ci:nodejs-$(NODE_VERSION)


### Cleanup ###
.PHONY: clean
clean:
	@echo "\nCleaning up leftover build/test directories..."
	rm -rf BUILD src/node_modules


### Setup ###
.PHONY: in_container/%
in_container/%:
	$(WITH_CONTAINER) make $*


### Production build, release and deploy ###
.PHONY: build_and_release
build_and_release: clean build zip release

.PHONY: install_prod
install_prod:
	@echo "\nInstalling dependencies for a production environment..."
	npm install --omit dev --prefix src

.PHONY: build
build: install_prod
	@echo "\nBuilding project in a node:$(NODE_VERSION) container..."
	mkdir BUILD
	cp -r src/* BUILD

.PHONY: zip
zip: BUILD
	@echo "\nZipping up the build directory..."
	cd $< && zip -9qr package.zip . \
		-x "*.test.js" \

.PHONY: release
release: BUILD/package.zip
	@echo "\nReleasing component $(COMPONENT_NAME) via Cosmos..."
	cosmos-release lambda --lambda-version=`cosmos-release generate-version $(COMPONENT_NAME)` $< $(COMPONENT_NAME)


### Development ###
# Call using `in_container/%` target eg./ `make in_container/test`
.PHONY: install_dev
install_dev:
	npm install --prefix src

.PHONY: test
test: install_dev
	npm test --prefix src
