import React, { Component, Fragment } from "react";
import ReactDOM from "react-dom";
import {
  HashRouter as Router,
  Route,
  Switch,
  Redirect,
} from "react-router-dom";

import Alert from "./layout/Alert";
import Header from "./layout/Header";
import Feed from "./posts/Feed";
import ForeignFeed from "./posts/ForeignFeed";
import Create from "./posts/Create";
import Post from "./posts/Post";
import ForeignPost from "./posts/ForeignPost";

import Landing from "./pages/Landing";
import Profile from "./pages/Profile";
import Inbox from "./pages/Inbox";
import GitHub from "./pages/GitHub";

import Login from "./auth/Login";
import Register from "./auth/Register";
import AuthRoute from "./auth/AuthRoute";

import { Provider } from "react-redux";
import { Provider as AlertProvider } from "react-alert";
import AlertTemplate from "react-alert-template-basic";

import store from "../store";
import { loadUser } from "../actions/auth";

const options = {
  timeout: 5000,
  position: "top center",
};

class App extends Component {
  componentDidMount() {
    store.dispatch(loadUser());
  }

  render() {
    return (
      <Provider store={store}>
        <AlertProvider template={AlertTemplate} {...options}>
          <Router>
            <Fragment>
              <Header />
              <div className="col-lg-6 mx-auto pt-4">
                <Alert />
                <Switch>
                  <AuthRoute exact path="/inbox" component={Inbox} />
                  <AuthRoute exact path="/posts" component={Feed} />
                  <AuthRoute exact path="/foreign" component={ForeignFeed} />
                  <AuthRoute exact path="/posts/create" component={Create} />
                  <AuthRoute
                    exact
                    path="/posts/:authorId/:postId"
                    component={Post}
                  />
                  <AuthRoute
                    exact
                    path="/foreign/posts/:postId"
                    component={ForeignPost}
                  />
                  <AuthRoute
                    exact
                    path="/github-activities"
                    component={GitHub}
                  />
                  <AuthRoute exact path="/profile/:id" component={Profile} />
                  <Route exact path="/" component={Landing} />
                  <Route exact path="/login" component={Login} />
                  <Route exact path="/register" component={Register} />
                </Switch>
              </div>
            </Fragment>
          </Router>
        </AlertProvider>
      </Provider>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));
