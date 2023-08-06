# StepWise Open edX Plugin

[![<pypi stepwise-edx-plugin](https://img.shields.io/static/v1?label=pypi&style=flat-square&color=0475b6&message=stepwise-edx-plugin)](https://pypi.org/project/stepwise-edx-plugin/) [![<Querium Stepwise Math](https://img.shields.io/static/v1?label=Querium&style=flat-square&color=ff5434&message=Stepwise%20Math)](https://stepwisemath.ai/) [![hack.d Lawrence McDaniel](https://img.shields.io/badge/hack.d-Lawrence%20McDaniel-orange.svg)](https://lawrencemcdaniel.com)

![Open edX](https://avatars.githubusercontent.com/u/40179672)

Implements custom features for the Open edX LMS and Studio applications using the new [pluggable extensibility](https://blog.lawrencemcdaniel.com/getting-started-with-open-edx-plugin-architecture/) model.


## Implements the following

### Querium StepWise Configuration API

Assigns the StepWise api server to use for the Open edX instance on which this plugin is installed.
The api endpoint is: https://web.stepwisemath.ai/stepwise/api/v1/configuration

source code is located in stepwise_plugin/api/

Uses this Django model: https://web.stepwisemath.ai/admin/stepwise_plugin/configuration/

public url to the api: https://web.stepwisemath.ai/stepwise/api/v1/configuration

### Wordpress CTA links

Provides a means to embed localization information about the user in CTA buttons that send the user from Wordpress to Open edX. The most common url presently is: https://web.stepwisemath.ai/stepwise/dashboard?language=es-419

source code is located in stepwise_plugin/dashboard/

### Localized Marketing Links

The reverse case. Provides a generalized way to seamlessly map the user from the LMS to the most sensible marketing site. An example usage is the "Discover New" link in the LMS site header. The url, assigned inside lms.yml within MKTG_URL_OVERRIDES is, https://web.stepwisemath.ai/stepwise/marketing-redirector/?stepwise_page=learning-content/ and will redirect to https://stepwisemath.ai/learning-content/ for a US-based user.

Uses this Django model: https://web.stepwisemath.ai/admin/stepwise_plugin/marketingsites/

### Localized html anchor tags

Same as above, but for html anchor tags. In addition to the URL mapping, these also require language translation of the text of the html element value, bearing in mind that we need to avoid changes to the edx-platform po files since we do not want to fork the edx-platform repo.

Uses this Django model: https://web.stepwisemath.ai/admin/stepwise_plugin/locale/

An example usage would be the "Blog" and "Privacy Policy" links in the LMS site footer. The following is added to the Mako template:

```mako
<%!
  from stepwise_plugin.locale.utils import anchor, language_from_request
%>

<%

  # figure out the best language code to use based on whatever we
  # know about this user.
  try:
    preferred_language = language_from_request(request) or 'en'
  except:
    preferred_language = 'en'

  # get a Python dict containing the url and element text.
  blog_dict = anchor('stepwise-locale-blog', preferred_language)
%>

```

and the link itself would take the form

```html
    <a id="stepwise-locale-blog" href="${blog_dict.get('url')}">${blog_dict.get('value')}</a>
```

### manage.py commands

```bash

# Create or update a Stepwise API server host configuration
./manage.py lms configure_stepwise_api --host 'https://stepwiseai01.querium.com/webMathematica/api/' --environment 'Production'

# Create or update a Stepwise marketing site configuration
./manage.py lms configure_stepwise_marketing_site --language en --site_url 'https://stepwisemath.ai/'

# Create or update Stepwise marketing site local html elements
./manage.py lms configure_stepwise_locale --element_id 'stepwise-locale-contact' --language 'es-419' --url 'https://mx.stepwisemath.ai/contact/' --value 'Contacto'

```

## Getting Started

### Install

#### Native

```bash
# where github-plugin is defined in .ssh/config
git clone git@github-plugin:QueriumCorp/stepwise-openedx-plugin.git -b main  /home/ubuntu/stepwise_plugin

sudo -H -u edxapp bash
source /edx/app/edxapp/edxapp_env
source /edx/app/edxapp/venvs/edxapp/bin/activate
pip install /home/ubuntu/stepwise_plugin
```

```python
# DO NOT!! add this near the bottom of /edx/app/edxapp/edx-platform/lms/envs/common.py

# NO! NO! NO! NO! NO! NO! NO! NO! NO! NO! NO! NO!
INSTALLED_APPS.extend('stepwise_plugin')    # DO NOT DO THIS!!!!!!
# NO! NO! NO! NO! NO! NO! NO! NO! NO! NO! NO! NO!

# it turns out that Open edX finds this package of its own accord.
# magical!!! :O
```

```bash
# to run tests
sudo -H -u edxapp bash
source /edx/app/edxapp/edxapp_env
source /edx/app/edxapp/venvs/edxapp/bin/activate
pip install -r requirements/edx/testing.txt
cd ~/edx-platform
./manage.py lms test stepwise_plugin --settings=test
```

### Local development

* Use the same virtual environment that you use for edx-platform
* Set your Python interpreter to 3.8x
* install black: https://pypi.org/project/black/
* install flake8: https://flake8.pycqa.org/en/latest/

```bash
# Run these from within your edx-platform virtual environment
pip3 install pre-commit
pre-commit install
pip3 install black
python3 -m pip install flake8
```

### Local development good practices

* run `black` on modified code before committing.
* run `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
* run `flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`
* run `pre-commit run --all-files` before pushing. see: https://pre-commit.com/

#### edx-platform dependencies

To avoid freaky version conflicts in prod it's a good idea to install all of the edx-platform requirements to your local dev virtual environment.

* requirements/edx/base.txt
* requirements/edx/develop.txt,
* requirements/edx/testing.txt

At a minimum this will give you the full benefit of your IDE's linter.

#### Notes regarding development with macOS M1

1. To avoid problems with installing the edx-platform requirements, create your virtual environment with Python >= 3.9.x using the native installer from https://www.python.org/. `which python` should return `/Library/Frameworks/Python.framework/Versions/3.9/bin/python3`. Ignoring this advise will lead to very weird side effects. Note that this is true even though Lilac actually runs on Python 3.8.x

2. Best to install openssl, openblas, zstd, mysql, and mysql-client with Brew. Using brew helps you avoid problems with gcc compilations and linking that have proven problematic on early releases of macOS 11 on M1. If you run into problems while pip installing mysql-client / MongoDBProxy / mongoengine/ pymongo /numpy / scipy / matplotlib then analyze the stack trace for any other straggling dependencies that I might have ommitted here that might also break due to the gcc compiler or linker, and try installing these instead with Brew.

3. In addition to launching your virtual environment it also helps to set the following environment variables in your terminal window. Make sure you pay attention to any further suggestions echoed in Brew installation output:

```bash
export OPENBLAS=/opt/homebrew/opt/openblas/lib/
export LDFLAGS="-L/opt/homebrew/opt/openblas/lib -L/opt/homebrew/opt/mysql-client/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openblas/include -I/opt/homebrew/opt/mysql-client/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/openblas/lib/pkgconfig /opt/homebrew/opt/mysql-client/lib/pkgconfig"
```

### Shell Plus and iPython

The stepwise_edxapi module adds ipython and django-extensions to the stack.  It is then possible to get an enhanced shell via:

```bash
tutor local exec lms ./manage.py lms shell_plus
```
