import { GET_GITHUB} from "../actions/types.js";

const initialState = {
  github_activity: [],
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_GITHUB:
        return {
            ...state,
            github_activity: action.payload
         };
    default:
      return state;
  }
}
