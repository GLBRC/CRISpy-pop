# Webpacker Info

Webpacker compiled files are located in `app/webpacker`

Webpacker configuration is at `config/webpacker.yml`

## To add a package to webpacker

```bash
yarn add xyz
```

## To compile assets on the fly

```bash
`./bin/webpack-dev-server`
```

## To add custom CSS or JS

1. Add the file you want to `app/webpacker/src` or `app/webpacker/stylesheets`
1. Import the file in the correct pack
1. `application.js` and `application.scss` are included in the default template, other packs must be included in their corresponding pages

## To use a react component in a view

```rails
<%= react_component("HelloWorld", { greeting: "Hello from react-rails." }) %>
```
