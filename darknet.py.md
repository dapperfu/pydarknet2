# ```darknet.py``` Usage.

```darknet.py```'s command line interface is built with [Click.](http://click.pocoo.org). When in doubt adding ```--help``` to the end of a command should give you some hints.

[Output clipped for brevity]

$ darknet.py --help

Commands:
  darknet  Manage darknet folder.
  weights  Manage darknet weights.


## darknet command group.

    $ darknet.py darknet --help

    Commands:
      build  Build darknet.
      clone  Clone a darknet repository.

### Clone

Clone a darknet repository:

    $ darknet.py darknet clone --help

        Options:
          --url url    Darknet clone url. [Default: https://github.com/jed-
                       frey/darknet.git]
          --root root  Darknet root directory. [Default:
                       ~/.darknet]
          --help       Show this message and exit.

### Build

Build the darknet binary and shared library:

    $ darknet.py darknet build --help

    Options:
      --root root  Darknet root directory. [Default:
                   ~/.darknet]
      --gpu        Compile with GPU support.
      --cudnn      Compile with cudnn support.
      --opencv     Compile with OpenCV support.
      --openmp     Compile with OpenMP support.
      --force      Do it.
      --help       Show this message and exit.
    
## weights command group.

*Note:* Default weight URL: https://functionalsafety.tech/darknet_weights/ is a mirror of *.weights available from https://pjreddie.com/media/files/ but hosted so I don't abuse his bandwidth.

### Available pretrained weights

List available pretrained weights:

    $ darknet.py weights available --help

    Options:
      --root root              Darknet root directory. [Default:
                               ~/.darknet]
      --weight_url weight_url  Pretrained weights url base. [Default:
                               https://functionalsafety.tech/darknet_weights/]
      --help                   Show this message and exit.

Example usage:

    $ darknet.py weights available
    # Available pretrained weights.
    # Download with: darknet.py weights download [weight]
    alexnet # Download cmd: darknet.py weights download alexnet
    cifar # Download cmd: darknet.py weights download cifar
    darknet # Download cmd: darknet.py weights download darknet
    darknet19 # Download cmd: darknet.py weights download darknet19
    darknet19_448 # Download cmd: darknet.py weights download darknet19_448
    ^C
    Aborted!

### Download pretrained weights

    $ darknet.py weights download --help

    Options:
      --root root              Darknet root directory. [Default:
                               ~/.darknet]
      --weight_url weight_url  Pretrained weights url base. [Default:
                               https://functionalsafety.tech/darknet_weights/]
      --weights weights        Pretrained weights directory. [Default:
                               ~/.darknet/weights]
      --help                   Show this message and exit.

Example usage:

    $ darknet.py weights download yolov3
    # Copy and paste this. Still manumatic
    curl --referer ... yolov3.weights

Generate a download script & run:
 
    $ darknet.py weights download yolov3 >> download.sh
    $ sh download.sh
    ############################################################################## 100.0%

### List downloaded pretrained weights

    $ darknet.py weights list --help
    
    Options:
      --root root        Darknet root directory. [Default:
                         ~/.darknet]
      --weights weights  Darknet weights directory [Default:
                         ~/.darknet/weights]
      --help             Show this message and exit.
    