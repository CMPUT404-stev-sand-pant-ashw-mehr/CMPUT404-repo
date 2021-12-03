import axios from "axios";
import store from "../../store";
import React, { Component, Fragment, useState } from "react";
import { connect } from "react-redux";

import ActivityCard from "../github/ActivityCard"
import PropTypes from "prop-types";
import {getGithub} from "../../actions/getGithub";

import { tokenConfig } from "../../actions/auth";
import { GET_ALERTS, GET_GITHUB } from "../../actions/types";


export class GithubActivity extends Component {
  constructor(props) {
    super(props);

    this.state = {
      Activities: [],
    };

  }

  
  componentDidMount() {
    const github = "shearpaladin" //idk how to grab the github of the user
    axios
        .get(`https://api.github.com/users/${github}/events/public` )
        .then(res => {
            console.log(res)
            this.setState({
                Activities: res.data
            });
        }).catch(err => {
            console.log(err)

        });
  }


  render() {
      let allActivities= this.state.Activities
      //console.log(allActivities)

      let display = 
              allActivities.length !== 0 && allActivities.map !== undefined ?
              allActivities.map((activity, index) => <ActivityCard key={index} activity={activity} />)
              :
              null
          
    return (
        <div>
            <h1> Git Activity</h1>
            {display}
        </div>
      
    );
  }

  static propTypes = {
    auth: PropTypes.object.isRequired,
    getGithub: PropTypes.func.isRequired
  };
}

const mapStateToProps = (state) => ({
    authorId: state.auth.user.author,
    auth: state.auth,
    github_activity: state.github_activity,
})

export default connect(mapStateToProps, {getGithub})(
  GithubActivity
);