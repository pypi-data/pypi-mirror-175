# Installing Calliope from PyPI

The simplest way to get Calliope is:

    pip3 install calliope-music

Some Calliope modules have
[extra dependencies](https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html)
which you need to install before the command will work.

Here's what happens if you run `cpe spotify` without installing its extra
dependencies first:

```
> cpe spotify top-artists
ERROR: Command 'spotify' is not available.

You can install this module's dependencies using `pip`, for example:

    pip install calliope-music[spotify]

    Original error: No module named 'cachecontrol'
```

To solve this, run `pip3 install calliope-music[spotify]` and rerun
the command.

# Installing Calliope with Meson

The project can be installed from the source tree using
[Meson](https://mesonbuild.com/).

An example of installing into your home directory:

    $ git clone --recursive https://gitlab.com/samthursfield/calliope/
    $ mkdir calliope/build
    $ cd calliope/build
    $ meson .. --prefix=$HOME/.local -Ddocs=false -Dtestsuite=false
    $ ninja install

You will likely see some missing dependency errors the first time you run
`meson`. Fix these either by installing the revelant packages, or by disabling
the feature in question.  See
[`meson_options.txt`](https://gitlab.com/samthursfield/calliope/-/blob/main/meson_options.txt)
for a list of available options.

Once this succeeds, the `cpe` binary will be in `$HOME/.local/bin` and should
be available in your `PATH`.

You can later enable documentation and/or the testsuite from inside the same
`build` directory:

    $ meson configure -Ddocs=true -Dtestsuite=true
