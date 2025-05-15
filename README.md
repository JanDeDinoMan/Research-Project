### MD
repo: <https://github.com/ikinsella/trefide>


The docker container is the best option because of dependency hell
```sh
docker run -it -p 3000:3000 -v ./Data:/root/trefide/Data -v ./trefide/demos:/root/trefide/demos janwillem/pmd:1.0
```


### CaiMan
repo: <https://github.com/flatironinstitute/CaImAn>

```sh
docker run -it -p 3000:3000 -v ./data:/root/caiman/data -v ./caiman/demos:/root/caiman/demos janwillem/caiman:1.0
```

```sh
conda activate caiman-env
```