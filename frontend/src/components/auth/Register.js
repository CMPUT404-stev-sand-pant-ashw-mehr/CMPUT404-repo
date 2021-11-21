import React, { Component } from "react";
import { Link, Redirect } from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { register } from "../../actions/auth";
import { createError } from "../../actions/alerts";

export class Register extends Component {
  state = {
    username: "",
    displayName: "",
    github: "",
    email: "",
    password: "",
    password_confirm: "",
  };

  onSubmit = (e) => {
    e.preventDefault();
    const { username, displayName, github, email, password, password_confirm } =
      this.state;
    if (password !== password_confirm) {
      this.props.createError("Passwords do not match!");
    } else {
      const user = {
        username,
        displayName,
        github,
        email,
        password,
      };
      this.props.register(user);
    }
  };

  onChange = (e) =>
    this.setState({
      [e.target.name]: e.target.value,
    });

  render() {
    if (this.props.auth.isAuthenticated) {
      return <Redirect to="/" />;
    }
    const { username, displayName, github, email, password, password_confirm } =
      this.state;
    return (
      <div className="row justify-content-center align-items-center">
        <div className="col-6">
          <form onSubmit={this.onSubmit}>
            <div className="mb-3">
              <label for="username" className="form-label">
                Username
              </label>
              <input
                className="form-control"
                type="text"
                name="username"
                onChange={this.onChange}
                value={username}
              />
            </div>
            <div className="mb-3">
              <label for="displayName" className="form-label">
                Display Name
              </label>
              <input
                className="form-control"
                type="text"
                name="displayName"
                onChange={this.onChange}
                value={displayName}
              />
            </div>
            <div className="mb-3">
              <label for="github" className="form-label">
                GitHub
              </label>
              <input
                className="form-control"
                type="text"
                name="github"
                onChange={this.onChange}
                value={github}
              />
            </div>
            <div className="mb-3">
              <label for="email" className="form-label">
                Email
              </label>
              <input
                className="form-control"
                type="email"
                name="email"
                onChange={this.onChange}
                value={email}
              />
            </div>
            <div className="mb-3">
              <label for="password" className="form-label">
                Password
              </label>
              <input
                className="form-control"
                type="password"
                name="password"
                onChange={this.onChange}
                value={password}
              />
            </div>
            <div className="mb-3">
              <label for="password_confirm" className="form-label">
                Confirm Password
              </label>
              <input
                className="form-control"
                type="password"
                name="password_confirm"
                onChange={this.onChange}
                value={password_confirm}
              />
            </div>
            <div className="mb-3">
              <button type="submit" className="btn btn-primary mx-auto">
                Register!
              </button>
            </div>
            <span>
              Already registered? <Link to="/login">Login</Link>
            </span>
          </form>
        </div>
      </div>
    );
  }
  static propTypes = {
    register: PropTypes.func.isRequired,
    auth: PropTypes.object.isRequired,
  };
}

const mapStateToProps = (state) => ({
  auth: state.auth,
});

export default connect(mapStateToProps, { register, createError })(Register);
