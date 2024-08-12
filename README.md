# Codechecker Wiifor

The codechecker has been integrated into the Wiifor github to be able to use our labels for analyzers (for example eslint)

The only difference between the Wiifor one and the main one is a script that creates specific labels for eslint (depending on the configuration)

First, clone the Wiifor codechecker project:

```bash
git clone git@github.com:wiifor/codechecker.git
git checkout eslint_labels
```

## Build the docker

```bash
docker build \
  --build-arg CC_REPO=https://github.com/wiifor/codechecker \
  --build-arg CC_VERSION=eslint_labels \
  --build-arg INSTALL_AUTH=no \
  --build-arg INSTALL_PSYCOPG2=no \
  --tag codechecker-wiifor:6.24.0 web/docker
```

## ... or pull the docker

```bash
docker login nexus.wiifor.com:8092
docker pull nexus.wiifor.com:8092/codechecker-wiifor:6.24.0
```

## Run the docker

```bash
docker run -d \
  -p 8001:8001 \
  -v /home/$USER/codechecker_workspace:/workspace \
  codechecker-wiifor:6.24.0
```

## Push on Nexus

```bash
# Tag to be pushed: replace <version> by what you need,e.g. 6.24.0
docker tag codechecker-wiifor:<version> nexus.wiifor.com:8092/codechecker-wiifor:<version>
# Push to nexus
docker push nexus.wiifor.com:8092/codechecker-wiifor:<version>
```

### Utils commands

## For cloud projects

```bash
# Pheobus
npx eslint -c ./src/.eslintrc.json src/* -f json -o eslint_pheobus.json
report-converter -t eslint -o ./codechecker_pheobus ./eslint_pheobus.json
CodeChecker store ./codechecker_pheobus/ -n Pheobus

# Mercure (using npx command from Pheobus)
npx eslint -c ./src/.eslintrc.json $REPO_ROOT_PATH/tools/mercure/custom-widgets/* -f json -o eslint_mercure.json
report-converter -t eslint -o ./codechecker_mercure ./eslint_mercure.json
CodeChecker store ./codechecker_mercure/ -n Mercure

```

## Create labels if eslint config changes

```bash
# In the codechecker repo
make venv
source venv/bin/activate

python3 scripts/labels/eslint.py --config-file LIST_FILES --label-file LABEL_FILE

# Exemple
python3 scripts/labels/eslint.py --config-file $REPO_ROOT_PATH/thingsboard/phoebus/.eslintrc.json $REPO_ROOT_PATH/thingsboard/phoebus/src/.eslintrc.json --label-file $CODECHECKER_PROJECT/config/labels/analyzers/eslint.json
```
