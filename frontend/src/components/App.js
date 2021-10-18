import React, { Component, Fragment } from "react";
import ReactDOM from "react-dom";

import Alert from "./layout/Alert";
import Header from "./layout/Header";
import Feed from "./posts/Feed";

import { Provider } from "react-redux";
import { Provider as AlertProvider } from "react-alert";
import AlertTemplate from "react-alert-template-basic";

import styled from "styled-components";

import store from "../store";

const options = {
  timeout: 5000,
  position: "top center",
};

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <AlertProvider template={AlertTemplate} {...options}>
          <Fragment>
            <Header />
            <Alert />
            <Feed />
          </Fragment>
        </AlertProvider>
      </Provider>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));
