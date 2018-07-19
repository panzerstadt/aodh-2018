import dummyData from "../../data/dummy/dummy_taipei";

export function fetchData(params) {
  return function(dispatch) {
    //http://35.189.128.32/v1/tweets/location/?lat=25.0330&lng=121.5654
    const { content } = params;

    if (window.debug.dummyJson) {
      //let dummyData = content ? dummyAfterData : dummyBeforeData;

      dummyData.results = Object.assign({}, dummyData.results, {
        content: content
      });

      dispatch({
        type: "FETCH_TWIT_FULFILLED",
        payload: dummyData
      });
      return;
    }

    // TODO:
    const url = new URL("http://35.189.128.32/v1/");
    Object.keys(params).forEach(key =>
      url.searchParams.append(key, params[key])
    );

    console.log("fetchTwit:", url);
    dispatch({ type: "FETCH_TWIT" });

    fetch(url, {
      credentials: "include"
    })
      .then(response => {
        return response.json();
      })
      .then(response => {
        response.results = Object.assign({}, response.results, {
          content: content
        });

        dispatch({
          type: "FETCH_TWIT_FULFILLED",
          payload: response
        });
      })
      .catch(err => {
        dispatch({ type: "FETCH_TWIT_REJECTED", payload: err.toString() });
      });
  };
}
