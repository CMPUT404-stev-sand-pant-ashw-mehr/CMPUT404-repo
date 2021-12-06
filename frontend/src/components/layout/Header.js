import React, { Component, Fragment } from "react";
import { Link, NavLink } from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { logout } from "../../actions/auth";

export class Header extends Component {
  render() {
    const { isAuthenticated, user, author } = this.props.auth;
    const authNavLinks = (
      <Fragment>
        <NavLink
          to="/feed"
          activeClassName="text-decoration-underline"
          className="me-3 py-2 text-dark text-decoration-none"
        >
          Feed
        </NavLink>
        <NavLink
          to="/authors"
          activeClassName="text-decoration-underline"
          className="me-3 py-2 text-dark text-decoration-none"
        >
          Authors
        </NavLink>
        <NavLink
          to="/github-activities"
          activeClassName="text-decoration-underline"
          className="me-3 py-2 text-dark text-decoration-none"
        >
          GitHub Activity
        </NavLink>
        <NavLink
          to="/posts/create"
          activeClassName="text-decoration-underline"
          className="me-3 py-2 text-dark text-decoration-none"
        >
          Create Post
        </NavLink>
        <NavLink
          to="/inbox"
          activeClassName="text-decoration-underline"
          className="me-3 py-2 text-dark text-decoration-none"
        >
          Inbox
        </NavLink>
        <a
          activeClassName="text-decoration-underline"
          className="nav-NavLink me-3 py-2 dropdown-toggle text-dark text-decoration-none"
          href="#"
          id="navbarDarkDropdownMenuNavLink"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          {user ? user.username + " " : ""}
          <img
            src={user ? author.github + ".png" : ""}
            style={{ height: 25 }}
            className="img rounded-circle"
          ></img>
        </a>
        <ul
          className="dropdown-menu dropdown-menu-dark"
          aria-labelledby="navbarDarkDropdownMenuNavLink"
        >
          <li>
            <NavLink
              to={`/profile/${user ? user.author : ""}`}
              className="dropdown-item btn btn-outline-primary me-2"
            >
              My Profile
            </NavLink>
          </li>
          <li>
            <a
              href="#"
              className="dropdown-item btn btn-outline-primary me-2"
              onClick={this.props.logout}
            >
              Logout
            </a>
          </li>
        </ul>
      </Fragment>
    );

    const guestNavLinks = (
      <Fragment>
        <Link to="/login" className="btn btn-outline-primary me-2">
          Login
        </Link>
        <Link to="/register" className="btn btn-primary">
          Register
        </Link>
      </Fragment>
    );

    return (
      <div>
        <div className="col-lg-6 mx-auto pt-4">
          <header>
            <div className="d-flex flex-column flex-md-row align-items-center pb-3 mb-4 border-bottom">
              <NavLink
                to={isAuthenticated ? "/feed" : "/"}
                className="d-flex align-items-center text-dark text-decoration-none"
              >
                <svg
                  width="76.13749999999999px"
                  height="70.4px"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="211.93125 39.8 76.13749999999999 70.4"
                  preserveAspectRatio="xMidYMid"
                >
                  <defs>
                    <filter
                      id="editing-extrusion"
                      x="-100%"
                      y="-100%"
                      width="300%"
                      height="300%"
                    >
                      <feFlood result="color1" flood-color="#444"></feFlood>
                      <feConvolveMatrix
                        order="8,8"
                        divisor="1"
                        kernelMatrix="1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1"
                        in="SourceAlpha"
                        result="extrude"
                      ></feConvolveMatrix>
                      <feComposite
                        in="color1"
                        in2="extrude"
                        result="comp-extrude"
                        operator="in"
                      ></feComposite>
                      <feOffset
                        dx="4"
                        dy="4"
                        in="comp-extrude"
                        result="offset-extrude"
                      ></feOffset>
                      <feMerge>
                        <feMergeNode in="offset-extrude"></feMergeNode>
                        <feMergeNode in="SourceGraphic"></feMergeNode>
                      </feMerge>
                    </filter>
                  </defs>
                  <g filter="url(#editing-extrusion)">
                    <g transform="translate(229.87500900030136, 86.19999980926514)">
                      <path
                        d="M13.02-14.78L13.02-14.78L13.02-14.78Q13.50-15.74 13.50-16.64L13.50-16.64L13.50-16.64Q13.50-17.54 13.41-18.03L13.41-18.03L13.41-18.03Q13.31-18.53 13.09-18.91L13.09-18.91L13.09-18.91Q12.61-19.74 11.65-19.74L11.65-19.74L11.65-19.74Q10.46-19.74 9.50-18.88L9.50-18.88L9.50-18.88Q8.48-17.98 8.48-16.58L8.48-16.58L8.48-16.58Q8.48-15.68 9.10-14.99L9.10-14.99L9.10-14.99Q9.73-14.30 10.69-13.66L10.69-13.66L10.69-13.66Q11.65-13.02 12.74-12.38L12.74-12.38L12.74-12.38Q13.82-11.74 14.78-10.98L14.78-10.98L14.78-10.98Q16.99-9.22 16.99-6.85L16.99-6.85L16.99-6.85Q16.99-5.25 16.14-3.89L16.14-3.89L16.14-3.89Q15.30-2.53 13.89-1.54L13.89-1.54L13.89-1.54Q10.82 0.64 6.75 0.64L6.75 0.64L6.75 0.64Q3.46 0.64 1.76-0.43L1.76-0.43L1.76-0.43Q0.06-1.50 0.06-3.14L0.06-3.14L0.06-3.14Q0.06-6.05 2.34-6.78L2.34-6.78L2.34-6.78Q2.98-7.01 3.95-7.01L3.95-7.01L3.95-7.01Q4.93-7.01 6.05-6.59L6.05-6.59L6.05-6.59Q5.54-5.28 5.54-4.10L5.54-4.10L5.54-4.10Q5.54-1.54 7.36-1.54L7.36-1.54L7.36-1.54Q8.54-1.54 9.52-2.40L9.52-2.40L9.52-2.40Q10.50-3.26 10.50-4.24L10.50-4.24L10.50-4.24Q10.50-5.22 9.87-5.92L9.87-5.92L9.87-5.92Q9.25-6.62 8.32-7.18L8.32-7.18L8.32-7.18Q7.39-7.74 6.32-8.29L6.32-8.29L6.32-8.29Q5.25-8.83 4.32-9.60L4.32-9.60L4.32-9.60Q2.14-11.36 2.14-14.18L2.14-14.18L2.14-14.18Q2.14-16 3.04-17.42L3.04-17.42L3.04-17.42Q3.94-18.85 5.38-19.81L5.38-19.81L5.38-19.81Q8.26-21.76 11.79-21.76L11.79-21.76L11.79-21.76Q15.33-21.76 17.04-20.70L17.04-20.70L17.04-20.70Q18.75-19.65 18.75-17.86L18.75-17.86L18.75-17.86Q18.75-16.29 17.54-15.30L17.54-15.30L17.54-15.30Q16.48-14.46 15.20-14.46L15.20-14.46L15.20-14.46Q13.92-14.46 13.02-14.78ZM40.19-13.28L40.19-13.28L40.19-13.28Q40.19 0.35 25.41 0.35L25.41 0.35L25.41 0.35Q23.04 0.35 19.14-0.22L19.14-0.22L22.72-19.14L22.72-19.14Q22.98-20.42 23.14-21.15L23.14-21.15L23.14-21.15Q28-21.50 30.16-21.50L30.16-21.50L30.16-21.50Q32.32-21.50 34.30-21.06L34.30-21.06L34.30-21.06Q36.29-20.61 37.60-19.62L37.60-19.62L37.60-19.62Q40.19-17.66 40.19-13.28ZM33.60-14.46L33.60-14.46L33.60-14.46Q33.60-19.23 30.18-19.23L30.18-19.23L29.86-19.23L29.86-19.23Q29.70-19.23 29.54-19.20L29.54-19.20L26.24-2.02L26.24-2.02Q26.37-1.95 26.50-1.95L26.50-1.95L26.75-1.95L26.75-1.95Q27.94-1.95 29.17-2.69L29.17-2.69L29.17-2.69Q30.40-3.42 31.36-4.93L31.36-4.93L31.36-4.93Q33.60-8.42 33.60-14.46Z"
                        fill="#ccc"
                      ></path>
                    </g>
                  </g>
                </svg>
                <span className="fs-5">Social Distribution</span>
              </NavLink>
              <nav className="d-inline-flex mt-2 mt-md-0 ms-md-auto">
                {isAuthenticated ? authNavLinks : guestNavLinks}
              </nav>
            </div>
          </header>
        </div>
      </div>
    );
  }

  static propTypes = {
    auth: PropTypes.object.isRequired,
    logout: PropTypes.func.isRequired,
  };
}

const mapStateToProps = (state) => ({
  auth: state.auth,
});

export default connect(mapStateToProps, { logout })(Header);
