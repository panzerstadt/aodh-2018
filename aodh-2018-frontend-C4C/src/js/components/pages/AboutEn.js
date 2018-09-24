import React, { Component } from "react";
import Typography from "@material-ui/core/Typography";
// import { createFilter } from "react-search-input";

// import List from "@material-ui/core/List";
// import ListItem from "@material-ui/core/ListItem";
// import ListItemIcon from "@material-ui/core/ListItemIcon";
// import ListItemText from "@material-ui/core/ListItemText";
// import Divider from "@material-ui/core/Divider";
// import TextField from "@material-ui/core/TextField";

const typographyStyle = {
  display: "inline",
  textDecoration: "none",
  color: "#50A2A7"
};

const selectedStyle = {
  display: "inline",
  padding: "5px 10px 5px 10px",
  backgroundColor: "#E9B44C",
  textDecoration: "none",
  color: "white"
};
export default class AboutEn extends Component {
  /*state = {
    keyword: ""
  };

  handleUpdate(e) {
    e.preventDefault();
    this.setState({ keyword: e.target.value });
  }*/

  render() {
    return (
      <div className="aboutEn" align="left">
        <p>
          <Typography component="p" color="textSecondary" align="right">
            <Typography
              style={typographyStyle}
              component="a"
              color="white"
              href="/about"
            >
              Japanese
            </Typography>{" "}
            /{" "}
            <Typography
              style={selectedStyle}
              component="a"
              color="#50A2A7"
              href="/aboutEn"
            >
              English
            </Typography>
          </Typography>
        </p>
        <font color="#444444">
          <h1> Sky as Subconscious Media </h1>
          <div align="center">
            <iframe
              width="450"
              height="253"
              src="https://www.youtube.com/embed/45T6I5MaNTU"
              frameborder="0"
              allow="autoplay; encrypted-media"
              allowfullscreen
            />
          </div>
          <h2> About this project </h2>
          <p>
            {" "}
            When we visit unfamiliar places for travel, or we encounter the
            disaster events, only information available in smart phones is not
            sufficient. In this work, we visualize the sentiments from the
            tweets of the place and show them in the sky. We help people
            subconsciously understand the atmosphere of the place.
          </p>
          <p>
            {" "}
            In our current life, AR is used only for limited purpose. But in
            near future, we will naturally use AR all time. This work shows you
            a vision in such era.
          </p>
          <p>
            {" "}
            The information we access with smart phones is the one we gather
            consciously. On the other hand, there is much more information we
            perceive subcosciously. Those are the changes of the weather,
            current time, direction we are facing, how comfortable the place is
            and so on.
          </p>
          <p>
            {" "}
            In this work, we suggest using the sky as a new form of media which
            affect people all the time even subcosciously. And adding new
            information to it, we can attain a new subconscious sense.
          </p>
          <p>
            {" "}
            For example, using AR, we can notice the situation of air pollution
            and criminal rate of the place visualized as color or haziness of
            the sky.
          </p>
          <p>
            {" "}
            If some accidents or disaster happen close to the place, we will
            notice them quickly by the change of sentiments, and the closest
            evacuation place will be shown if it is within range.
          </p>
          <p>
            {" "}
            As noted above, the sky can be a big canvas which can lead us to the
            new sense.
          </p>
          {/* <br />
          <div align="center">
            <iframe
              width="450"
              height="253"
              src="https://www.youtube.com/embed/TEmXSoDZ7Vk"
              frameborder="0"
              allow="autoplay; encrypted-media"
              allowfullscreen
            />
          </div>
          <br /> */}
          <h2> How we made this </h2>
          <p>
            {" "}
            There are six points for explaining our characteristic
            implementations.
          </p>
          <h3> 1) Sky detection using Deep Learning:</h3>
          <p>
            We use a scene parsing technology called PSPNet (Pyramid Scene
            Parsing Network). This achieved the highest accuracy in ImageNet
            Scene Parsing Challenge 2016. This technology is originally aiming
            for automatic driving and robot sensing etc. , so applying it in AR
            field is an innovative challenge.
          </p>
          <h3> 2) Double Sphere Mapping for soften the edge:</h3>
          <p>
            {" "}
            Even in PSPNet, of course the accuracy is not perfect. Sometimes the
            edge of detected sky is not accurate. So we map the scenery on the
            two surfaces around the user to soften the edge in appearance. The
            closer surface has an image which sky is removed as transparent,
            whereas the farer surface has full image. Between the surfaces the
            user can see the information appear on the sky. If the distance
            between the user and the spheres are sufficient, the users can see
            the scenery as a continuous image. So users can see it as an natural
            one even if the edge of the sky and buildings are inaccurate.
          </p>
          <h3> 3) Placing map on the sky with gazing UI for zooming:</h3>
          <p>
            {" "}
            We place the map on the sky as a way to check the map in AR space.
            It doesn’t prevent or bother the scenery, so it can be always there.
            And we also suggest the user interface for zooming up or down the
            map just by gazing at the top of the sky and gazing it off. This UI
            release users to use the additional pointing device.
          </p>
          <h3> 4) Sound source as gathering attention:</h3>
          <p>
            {" "}
            We want to notice the user where should be attentioned in an
            implicit way because our project pursue the methods for affecting
            the instinct sense of users. So we place the sound source at the
            place to be attentioned. Users can find the place by the difference
            of the sound volume between right and left ear. And it is more
            noticeable especially when they move their heads because the balance
            of the sound hearable by each ear changes according to the movement
            of the heads.
          </p>
          <h3> 5) Movement of Sentiments bar shows the freshness:</h3>
          <p>
            {" "}
            At first we want to show the information like aurora. That is
            beautiful and many people like the scenery. So in the sky we place
            the bars each of which shows the sentiments as color. And we design
            the movement showing how recent it is tweeted. The freshness is
            expressed as wider movement, length and altitude of the bar.
          </p>
          <h3>
            {" "}
            6) Showing the direction by huge flying circle and flow of
            fireflies:
          </h3>
          <p>
            {" "}
            In directing the users to the destination such as an evacuation
            place, we propose a new way to show a guide in AR space. We use the
            huge circle on the sky to position the point. The circle shrinks
            into the destination. This movement let the user notice in any case
            the user is facing to. And as another suggestion, many fireflies are
            flying through the user. User will follow them instinctly. This
            utilizes an effect of crowd psychology.
          </p>
          <br />
          <h2>About us</h2>
          <p>
            We “STANDY” are a team formed in ASIA OPEN DATA HACKATHON 2017 held
            among four Asian countries and won the top prize there.
          </p>
          <p>
            Members in AODH2018: 　Koichi Okada (JAPAN) Rohit Kumar Singh
            (INDIA) Tang Li Qun (MALAYSIA) Satoshi Yanagisawa (JAPAN)
          </p>
          <br />
          <br />
          <br />
          <h2 align="left"> Resources </h2>
          <p align="left">
            <a href="https://1drv.ms/p/s!Ajr-EdBHcZP-gf48aYwElgUhHh64CA">
              {" "}
              Powerpoint presentation (35MB)
            </a>
            <br />
            <a href="https://github.com/panzerstadt/aodh-2018">
              {" "}
              Github repository
            </a>
          </p>
          <br />
          <br />
          <br />
        </font>
      </div>
    );
  }
}
