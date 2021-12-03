import React from 'react'
import {makeStyles} from '@mui/styles';

import {
  FaGithubSquare
} from "react-icons/fa";

//Documentation: https://mui.com/styles/basics/

const useStyles = makeStyles({
    root: {

    },
    github_title: {
        display: "flex",
        fontSize: "40px",
		paddingTop: "11px",
		paddingRight: "10px",
        white_space: "nowrap",
    },

    author_info: {
        color:'#H3H3H3',
        fontSize: '0.75em',
        padding:'0em 2em',
        paddingTop:'1em'
    },
    divider: {
        margin: '0em 1em',
        opacity: '0.5'
    },

    box: {
        boxShadow: '1px 3px 1px #9E9E9E',
        float: "left",
        marginRight: "10px",
        borderStyle: "solid"
    }

  

});


export default function ActivityCard(props) {
    const classes = useStyles();

    return (

        <div className="box">
            <span className="github_title">
                <FaGithubSquare/> 
                <h4>{props.activity.type}</h4>
            </span>
                <p className={classes.author_info}>
                    Posted by {props.activity.actor.display_login} on {props.activity.created_at.split('T')[0]}
                </p>
                <hr className={classes.divider}></hr>
        </div>
    )
}