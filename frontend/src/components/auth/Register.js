import React, { Component } from "react";
import { Link, Redirect } from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { register } from "../../actions/auth";
import { createError } from "../../actions/alerts";

export class Register extends Component {
  state = {
    username: "",
    email: "",
    password: "",
    password_confirm: "",
  };

  onSubmit = (e) => {
    e.preventDefault();
    const { username, email, password, password_confirm } = this.state;
    if (password !== password_confirm) {
      this.props.createError("Passwords do not match!");
    } else {
      const user = {
        username,
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
    const { username, email, password, password_confirm } = this.state;
    return (
      <div>
        <form onSubmit={this.onSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              className="form-control"
              type="text"
              name="username"
              onChange={this.onChange}
              value={username}
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              className="form-control"
              type="email"
              name="email"
              onChange={this.onChange}
              value={email}
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              className="form-control"
              type="password"
              name="password"
              onChange={this.onChange}
              value={password}
            />
          </div>
          <div className="form-group">
            <label>Confirm Password</label>
            <input
              className="form-control"
              type="password"
              name="password_confirm"
              onChange={this.onChange}
              value={password_confirm}
            />
          </div>
          <div className="form-group">
            <button type="submit" className="btn btn-primary">
              Register!
            </button>
          </div>
          <br />
          <span>
            Already registered? <Link to="/login">Login</Link>
          </span>
        </form>
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
