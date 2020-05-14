### Apollo Whitepaper

https://eprint.iacr.org/2016/1037.pdf


### Build the service

First, you need to build the local base image by running `docker-compose build base`.


### Run tests

`docker-compose run --rm app python manage.py test --settings config.settings.test`

or enter `./backend` and run `./run_all_tests.sh`


### Run the service

`docker-compose up`

and visit `localhost` to visit main page or
`localhost/api` to see the API.


### Hot reloading apollo-crypto

Whenever you make changes in apollo-crypto and you want them to be reflected in backend or frontend, you need to compile the code appropriately.

* To refresh the frontend enter `apollo-crypto-wasm` and run `wasm-pack build`.
* To refresh the backend run `docker-compose exec app pip install /apollo-crypto-python`

### Enter django shell

`docker-compose run --rm app python manage.py shell_plus --ipython`

### Troubleshooting

##### My `web` container doesn't get up
Try entering the container via
`docker-compose run --rm --entrypoint bash web` and running `yarn install`.

##### I have some weird stuff in my database that keeps breaking things
You can clean the whole database by using `docker-compose down`.
For now we don't use persistent volumes.


##### My app is unstable - I keep getting 502 and it works slowly

Sometimes traefik does weird things. Usually it helps to just run `docker-compose restart app traefik`
and it will again resolve the routes properly.
