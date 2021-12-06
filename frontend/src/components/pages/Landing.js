import React, { Component, Fragment } from "react";
import { Redirect, Route } from "react-router-dom";

export class Landing extends Component {
  render() {
    const isLoggedIn = localStorage.getItem("token") != null;

    return (
      <Route
        render={() =>
          !isLoggedIn ? (
            <Fragment>
              <h1>Landing</h1>
            </Fragment>
          ) : (
            <Redirect to={{ pathname: "/feed" }} />
          )
        }
      />
    );
  }

  static propTypes = {};
}

export default Landing;
