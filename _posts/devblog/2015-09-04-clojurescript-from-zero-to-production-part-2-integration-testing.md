---
category: programming
title: "ClojureScript: From Zero to Production (Part 2) - Integration Testing"
tagline: "PugglePay dev blog"
description: "Autorunning browser integration specs for a single page ClojureScript app, with Leiningen, clj-webdriver and speclj."
tags: [clojurescript, clojure]
---
If you are building a single page ClojureScript app, you might be
wondering how to write integration specs for it. By integration specs,
I mean tests that are run in the browser against a build that is as
close to the production app as possible.

In this post, I'll show you our setup to get autorunning integration
tests using `leiningen`, `clj-webdriver` and `speclj`.

<!-- more -->

## Goal

The goal is to get the integration tests to be run every time we save
a file. Getting to run individual tests from the REPL was not a goal
here, because we did not want to force the developers to have any
particular integration with their editors to get a good development
experience.

## Dependencies

We need to run the tests in a browser that is "driveable" by
WebDriver. We chose [phantomjs](https://github.com/ariya/phantomjs)
because it's easy to install and fast enough.

You can install it with `apt-get install phantomjs`, `brew install
phantomjs`, or your favourite package manager.

## Setting up your project.clj

You'll need a new build target in your `project.clj`.

Note: this assumes you're using leiningen. If you're using boot, there
might be a better way to do all this.

Before adding integration tests, your `project.clj` should look something like this:

```clojure
(defproject my-project "0.1.0-SNAPSHOT"
  :description "FIXME: write this!"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}

  :dependencies [[org.clojure/clojure "1.7.0"]
                 [org.clojure/clojurescript "1.7.48"]]

  :plugins [[lein-cljsbuild "1.0.6"]]

  :source-paths ["src"]

  :resource-paths ["resources" "resources/public"]

  :cljsbuild
  {:builds
   {:main {:source-paths ["src"]
           :compiler {:output-to "resources/public/out/my_project.js"
                      :optimizations :advanced
                      :main my-project.core
                      :pretty-print false}}}}

  :profiles
  {:dev {:dependencies [[figwheel "0.3.8"]
                        [org.clojure/tools.nrepl "0.2.10"]]
         :plugins [[lein-figwheel "0.3.8"]]

         :cljsbuild
         {:builds
          {:main {:source-paths ["src"]
                  :figwheel {:on-jsload "my-project.core/on-js-reload"}
                  :compiler {:main my-project.core
                             :optimization :none
                             :asset-path "out"
                             :output-to "resources/public/out/my_project.js"
                             :output-dir "resources/public/out"
                             :source-map-timestamp true}}}}

         :figwheel {:css-dirs ["resources/public/css"]}

         :clean-targets ^{:protect false} ["resources/public/js/compiled" "target"]}})
```

Let's add a new profile for integrations specs with all the extra
dependencies we need:

```clojure
   :integration {:dependencies [[compojure "1.3.4"]
                                [ring/ring-jetty-adapter "1.4.0-RC1"]
                                [clj-webdriver "0.6.1"]
                                [speclj "3.3.1"]]

                 :plugins [[speclj "3.2.0"]]

                 :test-paths ["src" "spec"]}
```

If we dissect the above, we're adding compojure and a ring jetty
adapter so we can serve our compile app to a browser, `clj-webdriver`
will be interacting with the browser and `speclj` will be used to run
the test. Note that `speclj` could be replaced with any other testing
library.

We'll put our tests in a separate `spec` folder at the root of the
project, that's why we add it to the test paths.

## Setup the tests

To run the integration tests, and every time we save one of the source
files, we need the following steps:

* Compile the ClojureScript app

* Start a webserver to serve the app

* Setup a WebDriver that can visit the app served by the webserver.

Using `speclj`, this will mean adding a bunch of wrappers around our
actual specs.

Let's start with writting a webserver that will help us serve our app
in `spec/my_project/spec_utils/server.clj`:

```clojure
(ns my.project.spec-utils.server
  (:require [clojure.java.io :as io]
            [compojure.core :refer [routes GET defroutes]]
            [compojure.route :refer [resources]]
            [compojure.handler :refer [api]]
            [ring.adapter.jetty :refer [run-jetty]]))

(defroutes http-handler
  (resources "/" :root "resources/public"))

(defn start [port]
  (run-jetty http-handler {:port port :join? false}))
```

This is a very simple server that will server all static files from
the `resources/public` folder.

Next, let's add a compiler in `spec/my_project/spec_utils/compiler.clj`:

```clojure
(ns my-project.spec-utils.compiler
  (:require [cljs.build.api]))

(defn build-cljs!
  "Builds cljs for integration specs"
  []
  (println "building cljs")
  (cljs.build.api/build
   "src"
   {:main 'my-project.core
    :output-to "resources/public/integration/main.js"
    :output-dir "resources/public/integration"
    :asset-path "integration"
    :optimizations :none
    :static-fns true ; for phantomjs/safari
    }))
```

And finally, we'll need the phantomjs driver (`spec/my_project/spec_utils/phantomjs.clj`):

```clojure
(ns my-project.spec-utils.phantomjs
  (:import [org.openqa.selenium.phantomjs PhantomJSDriver]
           [org.openqa.selenium.remote DesiredCapabilities]))

(defn driver []
  (PhantomJSDriver.
   (doto (DesiredCapabilities.)
     (.setCapability "phantomjs.cli.args"
                     (into-array String ["--ignore-ssl-errors=true"
                                         "--webdriver-loglevel=warn"])))))
```

There's a bit of Java incantations here to parametrize the
driver. Webdriver is using the Java version of the Selenium webdriver,
so if you want to configure this further you can look into Selenium's
docs.

Finally, let's create a single-entry utils file
`spec/my_project/spec_utils.clj` to combine all of the above:

```clojure
(ns my-project.spec-utils
  (:require [clj-webdriver.taxi :as t]
            [clj-webdriver.driver :as driver]
            [my-project.spec-utils.server :as server]
            [my-project.spec-utils.compiler :as compiler]
            [my-project.spec-utils.phantomjs :as phantomjs]))

(def build-cljs! compiler/build-cljs!)

(defn with-server
  "Start a server to host the js files"
  [specs]
  (println "starting server")
  (let [svr (server/start 10555)]
    (try (specs) (finally (.stop svr)))))

(defn with-webdriver
  "setup selenium webdriver"
  [specs]
  (println "starting webdriver")
  (try
    (let [driver (driver/init-driver {:webdriver (phantomjs/driver)})]
      (t/implicit-wait driver 3000)
      (t/set-driver! driver)
      (specs))
    (finally (t/quit))))
```

Then we're ready to write our first spec! In
`spec/my_project/core_spec.clj`:

```clojure
(ns my-project.core-spec
  (:require [clj-webdriver.taxi :as taxi]
            [speclj.core :refer :all]
            [my-project.spec-utils :as utils]))

(describe "the whole thing"
  (before-all (utils/build-cljs!))
  (around-all [specs] (utils/with-server specs))
  (around-all [specs] (utils/with-webdriver specs))

  (describe "index page"
    (it "works"
      (taxi/to "http://localhost:10555/")
      (taxi/take-screenshot :file "./screenshot.png")
      (should-contain "hello!" (taxi/text "h2")))))
```

## Result

You can find an example of minimal setup here: [https://github.com/Jell/cljs-autospec-example](https://github.com/Jell/cljs-autospec-example).

This follows closely the instructions in this blogpost.

## Extra tips

In our setup, we duplicate the compiler options several times: twice
in the `project.clj` and once in `compiler.clj`.

This can be tedious and error-prone if you have `:libs` or
`:foreign-libs` in your config.

To avoid this, you can move the common compiler options to a separate
`config/compiler.clj` file that you then read in your `project.clj`
and `compiler.clj` files.

Do do that in the `project.clj`, use an unquoted expression:

```clojure
{:compiler ~(read-string (slurp "config/compiler.clj"))}
```
