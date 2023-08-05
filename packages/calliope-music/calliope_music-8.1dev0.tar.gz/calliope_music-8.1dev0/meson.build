project('calliope',
        version: '8.1dev0',
        meson_version: '>= 0.53')

cdata = configuration_data()

# Process the feature dependecies.
#
# We use the 'feature' option where possible because it allows users to
# easy opt-in to every feature (set auto_features=enabled) or opt-out of
# every feature (set auto_features=disabled).
#
# Some of the requirements are not yet specified here.
#
dependency('libgstreamer-1.0', required: get_option('play'))
libmediart = dependency('libmediaart-2.0', required: get_option('tracker'))
dependency('tracker-sparql-3.0', required: get_option('tracker'))

# Requires bundled lastfmclient library
cdata.set('enable_lastfm', get_option('lastfm').auto() or get_option('lastfm').enabled())

# WIP
cdata.set('enable_suggest', get_option('suggest').auto() or get_option('suggest').enabled())

# Requires GTK, etc.
cdata.set('enable_viewer_app', get_option('viewer').auto() or get_option('viewer').enabled())


###############################################################################
# Python dependencies
###############################################################################

pymod = import('python')

base_modules = []
if get_option('check_runtime_deps')
  base_modules = ['setuptools']
endif

python = pymod.find_installation('python3', modules: base_modules)

if not python.language_version().version_compare('>= 3.7')
  error('Python 3.7 or newer is required.')
endif

#install_requires = [
#  'click',
#  'jsonschema',
#  'parsedatetime',
#  'pyyaml',
#  'splitstream',
#]
#
feature_install_requires = {
  'bandcamp': ['beautifulsoup4', 'requests'],
  'listenbrainz': [],
  'musicbrainz': ['musicbrainzngs >= 0.7'],
  'play': ['gi'],
  'select': ['simpleai'],
  'spotify': ['cachecontrol', 'lockfile', 'spotipy'],
  'tracker': ['gi'],
  'youtube': ['google-api-python-client'],
}
#
#setup_requires = [
#]
#
test_requires = [
  'mutagen', 'pytest-benchmark', 'pytest-pep8',
]
#
doc_requires = [
  'sphinx', 'sphinx-autoapi', 'sphinx-click', 'sphinx-jsonschema',
]
#
#missing_dependency_errors = []
#
#message('Checking for core Python dependencies')
#modules_check = run_command(python, 'meson-python-packages-check', install_requires + setup_requires, check: false)
#if modules_check.returncode() != 0
#  error('Python dependency requirements are not satisfied:\n' + modules_check.stderr().strip())
#endif
#
foreach feature_name, deps : feature_install_requires
#  message('Checking for Python dependencies for feature ' + feature_name)
  option_name = 'enable_' + feature_name
#  if get_option(feature_name).auto() or get_option(feature_name).enabled()
#    modules_check = run_command(python, 'meson-python-packages-check', deps, check: false)
#    if modules_check.returncode() == 0
      cdata.set(option_name, true)
#    else
#      if get_option(feature_name).enabled()
#        error('Python dependency requirements are not satisfied for @0@: @1@\n'.format(feature_name, modules_check.stderr().strip()))
#      else
#        cdata.set(option_name, false)
#      endif
#    endif
#  else
#    cdata.set(option_name, false)
#  endif
endforeach
#
if get_option('docs')
  message('Checking for Python documentation dependencies')
  modules_check = run_command(python, 'meson-python-packages-check', doc_requires, check: false)
  if modules_check.returncode() != 0
    error('Documentation dependency requirements are not satisfied:\n' + modules_check.stderr().strip())
  endif

  sphinx_apidoc = find_program('sphinx-apidoc-3', 'sphinx-apidoc', required: true)
  sphinx_build = find_program('sphinx-build-3', 'sphinx-build', required: true)
endif
#
if get_option('testsuite')
  message('Checking for Python test suite dependencies')
  modules_check = run_command(python, 'meson-python-packages-check', test_requires, check: false)
  if modules_check.returncode() != 0
    error('Test suite dependency requirements are not satisfied:\n' + modules_check.stderr().strip())
  endif

  pylint = find_program('pylint-3', 'pylint')

  pytest = find_program('pytest-3', 'pytest')
endif

###############################################################################
# Configuration
###############################################################################

localedir = join_paths(get_option('prefix'), get_option('localedir'))
pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), 'tagcloud')

cdata.set('localedir', localedir)
cdata.set('pkgdatadir', pkgdatadir)
cdata.set('pythonsitepackagesdir', python.get_install_dir())
cdata.set('version', meson.project_version())

top_source_dir = meson.current_source_dir()
top_build_dir = meson.current_build_dir()

run_from_source_tree = find_program('scripts/run_from_source_tree', required: true)

subdir('calliope')
subdir('data')

if cdata.get('enable_viewer_app')
  subdir('apps/viewer')
endif

if get_option('testsuite')
  subdir('tests')
endif

subdir('examples')

if get_option('docs')
  subdir('docs')
endif

summary({
    'Documentation': get_option('docs'),
    'Test suite': get_option('testsuite'),
  }, section: 'Build')

summary({
    'bandcamp': cdata.get('enable_bandcamp'),
    'lastfm': cdata.get('enable_lastfm'),
    'listenbrainz': cdata.get('enable_listenbrainz'),
    'musicbrainz': cdata.get('enable_musicbrainz'),
    'play': cdata.get('enable_play'),
    'select': cdata.get('enable_select'),
    'spotify': cdata.get('enable_musicbrainz'),
    'suggest': cdata.get('enable_suggest'),
    'tracker': cdata.get('enable_tracker'),
    'youtube': cdata.get('enable_youtube'),
  }, section: 'Features'
)
