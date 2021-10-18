import React from "react";
import { connect } from "react-redux";
import { Route, Redirect } from "react-router-dom";

const AuthRoute = ({ component: Component, auth, ...rest }) => (
  <Route
    {...rest}
    render={(props) => {
      if (auth.isLoading) {
        return <span>Loading</span>;
      } else if (!auth.isAuthenticated) {
        return <Redirect to="/login" />;
      }

      return <Component {...props} />;
    }}
  />
);

const mapStateToProps = (state) => ({ auth: state.auth });

export default connect(mapStateToProps)(AuthRoute);
