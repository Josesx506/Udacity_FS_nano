# Coffee Shop Frontend

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman, and then the frontend should integrate smoothly.

### Installing Dependencies

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing Ionic Cli

The Ionic Command Line Interface is required to serve and build the frontend. Instructions for installing the CLI is in the [Ionic Framework Docs](https://ionicframework.com/docs/installation/cli).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: **npm i** is shorthand for **npm install**

## Required Tasks

### Configure Environment Variables

Ionic uses a configuration file to manage environment variables. These variables ship with the transpiled software and should not include secrets.

- Open `./src/environments/environments.ts` and ensure each variable reflects the system you stood up for the backend.

## Running Your Frontend in Dev Mode

Ionic ships with a useful development server which detects changes and transpiles as you work. The application is then accessible through the browser on a localhost port. To run the development server, cd into the `frontend` directory and run:

```bash
ionic serve
```

> _tip_: Do not use **ionic serve** in production. Instead, build Ionic into a build artifact for your desired platforms.
> [Checkout the Ionic docs to learn more](https://ionicframework.com/docs/cli/commands/build)

## Key Software Design Relevant to Our Coursework

The frontend framework is a bit beefy; here are the two areas to focus your study.

### Authentication

The authentication system used for this project is Auth0. `./src/app/services/auth.service.ts` contains the logic to direct a user to the Auth0 login page, managing the JWT token upon successful callback, and handle setting and retrieving the token from the local store. This token is then consumed by our DrinkService (`./src/app/services/drinks.service.ts`) and passed as an Authorization header when making requests to our backend.

### Authorization

The Auth0 JWT includes claims for permissions based on the user's role within the Auth0 system. This project makes use of these claims using the `auth.can(permission)` method which checks if particular permissions exist within the JWT permissions claim of the currently logged in user. This method is defined in  `./src/app/services/auth.service.ts` and is then used to enable and disable buttons in `./src/app/pages/drink-menu/drink-form/drink-form.html`.


### Additional frontend setup local implementation on Intel Macbook
I originally installed node with brew using `brew install node`. This installed node v21.4.0 which was giving me issues with running ionic serve. Turns out I couldn't downgrade node with brew so I had to install `nvm`.
1. Install **nvm**
    - ```bash
        # Uninstall the brew version of node
        ~ $brew uninstall node --force
        # Install node version manager (nvm)
        ~ $brew install nvm
        # You should create NVM's working directory if it doesn't exist
        ~ $mkdir ~/.nvm
        ```
2. After installation, add the following lines to your `~/.bash_profile` or `~/.bashrc` file to set the path for nvm
    - ```bash
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
        ```
3. Install a lower node version. I installed `v16.20.2` and the lts version `v20.10.0`
    - ```bash
        ~ $nvm install 16.20.2
        # Install the lts version which is required by ionic/cli@7.1.5
        ~ $nvm install --lts
        # Set the nvm version for ionic cli
        ~ $nvm use --lts
        # Set the default version for other npm install with "nvm alias default <version>"
        ~ $nvm alias default 16.20.2
        ```
    - You can uninstall specific versions with `nvm uninstall 16.20.2`
4. View installed nvm versions with `nvm list`. It should return an output similar to this
    - ```bash
        ->     v16.20.2
            v20.10.0
        default -> 16.20.2 (-> v16.20.2)
        iojs -> N/A (default)
        unstable -> N/A (default)
        node -> stable (-> v20.10.0) (default)
        stable -> 20.10 (-> v20.10.0) (default)
        lts/* -> lts/iron (-> v20.10.0)
        lts/argon -> v4.9.1 (-> N/A)
        lts/boron -> v6.17.1 (-> N/A)
        lts/carbon -> v8.17.0 (-> N/A)
        lts/dubnium -> v10.24.1 (-> N/A)
        lts/erbium -> v12.22.12 (-> N/A)
        lts/fermium -> v14.21.3 (-> N/A)
        lts/gallium -> v16.20.2
        lts/hydrogen -> v18.19.0 (-> N/A)
        lts/iron -> v20.10.0
        ```
5. Install ionic cli with `npm install -g @ionic/cli`. You can specify a version too e.g `npm install -g @ionic/cli@6.0.0 -f`
    - I had multiple issues with the cli so I had to uninstall it multiple times. `npm uninstall -g @ionic/cli` didn't work several times, so I resorted to deleting the folder with `rm -rf /usr/local/lib/node_modules/@ionic` or `$NVM_DIR/versions/node/v16.20.2/lib/node_modules/@ionic` as a way of uninstalling.
6. After going through **steps 1-5**, you should also be able to see the node and npm versions, as well as the ionic cli version with
    - ```bash
        ~ $node -v
        v16.20.2
        ~ $npm -v
        8.19.4
        ~ $npm list -g
        /Users/josesmac/.nvm/versions/node/v16.20.2/lib
        ├── @ionic/cli@7.1.5
        ├── corepack@0.17.0
        └── npm@8.19.4
        ```
7. I was having some issues with openssl but that seemed to stop after I downgraded the node version. Next step was to install the node modules in `03_coffee_shop/frontend folder`.
    - ```bash
        # navigate to the folder
        ~ $cd 03_coffee_shop/frontend folder
        # Delete the old package lock file
        frontend $rm package-lock.json
        # Install the node modules
        frontend $npm install
        # Fix any dependency issues without forcing it
        frontend $npm audit fix
        ```
8. After all this, the frontend still wasn't launching, then I checked the knowledge center for other students with similar problems. One problem was with `node-sass`. A fix from stackoverflow was linked https://stackoverflow.com/questions/74700023/error-node-sass-version-8-0-0-is-incompatible-with-4-0-0/74791591#74791591.
    - ```bash
        # Uninstall node-sass
        frontend $npm uninstall node-sass
        # Reinstall sass
        frontend $npm install sass
        # Launch the server with ionic
        frontend $ionic serve
        ```
