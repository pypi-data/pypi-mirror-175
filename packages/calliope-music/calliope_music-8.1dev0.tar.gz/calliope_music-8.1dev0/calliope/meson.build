sources = files(
  '__init__.py',
  '__main__.py',
  'cache.py',
  'cli.py',
  'config.py',
  'playlist.py',
  'resolvers.py',
  'sync_operation.py',
  'utils.py',
)

jsonschema = files(
  'playlist-item.jsonschema',
)

python.install_sources(
    sources + jsonschema,
    subdir: 'calliope')

configure_file(
    input: 'modules.conf.in',
    output: 'modules.conf',
    configuration: cdata,
    install_dir: join_paths(python.get_install_dir(), 'calliope'))

configure_file(
    input: 'main.py.in',
    output: 'cpe',
    configuration: cdata,
    install_dir: get_option('bindir'))

# Sources for the whole 'calliope' module. This variable is appended to by the
# meson.build files inside the package subdirectories.
calliope_module_sources = sources
calliope_jsonschema = jsonschema

subdir('beets')
subdir('diff')
subdir('export')
subdir('import_')
subdir('shuffle')
subdir('stat')
subdir('sync')
subdir('validate')

if cdata.get('enable_bandcamp')
  subdir('bandcamp')
endif

if cdata.get('enable_lastfm')
  subdir('lastfm')
endif

if cdata.get('enable_listenbrainz')
  subdir('listenbrainz')
endif

if cdata.get('enable_musicbrainz')
  subdir('musicbrainz')
endif

if cdata.get('enable_play')
  subdir('play')
endif

if cdata.get('enable_select')
  subdir('select')
endif

if cdata.get('enable_spotify')
  subdir('spotify')
endif

if cdata.get('enable_suggest')
  subdir('suggest')
endif

if cdata.get('enable_tracker')
  subdir('tracker')
endif

if cdata.get('enable_youtube')
  subdir('youtube')
endif

subdir('subprojects')
