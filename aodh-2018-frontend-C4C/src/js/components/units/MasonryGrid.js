import * as React from "react";
import Masonry from "react-masonry-component";
import SimpleCard from "./SimpleCard";

const masonryOptions = {
  transitionDuration: 500,
  fitWidth: "true"
};

const masonryStyle = {
  margin: "auto",
  marginTop: 20
};

const imagesLoadedOptions = { background: ".my-bg-image-el" };

class Gallery extends React.Component {
  render() {
    const childElements = this.props.data.map((data, i) => {
      // return <SimpleCard data={data} />;
      return <SimpleCard key={i} data={data} />;
    });

    return (
      <Masonry
        className={"my-gallery-class"} // default ''
        elementType={"div"} // default 'div'
        style={masonryStyle}
        options={masonryOptions} // default {}
        disableImagesLoaded={false} // default false
        updateOnEachImageLoad={false} // default false and works only if disableImagesLoaded is false
        imagesLoadedOptions={imagesLoadedOptions} // default {}
      >
        {childElements}
      </Masonry>
    );
  }
}

export default Gallery;
