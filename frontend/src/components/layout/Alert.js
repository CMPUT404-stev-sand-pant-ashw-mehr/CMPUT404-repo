import React, { Component, Fragment } from "react";
import { withAlert } from "react-alert";
import { connect } from "react-redux";
import PropTypes from "prop-types";

export class Alert extends Component {
  componentDidUpdate(prevProps) {
    const { alert, alerts } = this.props;
    if (alerts !== prevProps.alerts) {
      for (var msg in alerts.msg) {
        if (msg == "success") {
          alert.success(`${alerts.msg[msg]}`);
        } else {
          if (alerts.msg[msg] instanceof Array) {
            alert.error(`${alerts.msg[msg].join(", ")}`);
          } else {
            alert.error(`${alerts.msg[msg]}`);
          }
        }
        break;
      }
    }
  }

  render() {
    return <Fragment />;
  }

  static propTypes = {
    alerts: PropTypes.object.isRequired,
  };
}

const mapStateToProps = (state) => ({
  alerts: state.alerts,
});
export default connect(mapStateToProps)(withAlert()(Alert));
