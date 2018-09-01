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

export default class About extends Component {
  /* state = {
    keyword: ""
  };

  handleUpdate(e) {
    e.preventDefault();
    this.setState({ keyword: e.target.value });
  }*/

  render() {
    return (
      <div className="about" /* id="about" */>
        <p>
          <Typography component="p" color="textSecondary" align="right">
            <Typography
              style={selectedStyle}
              component="a"
              color="white"
              href="/about"
            >
              Japanese
            </Typography>{" "}
            /{" "}
            <Typography
              style={typographyStyle}
              component="a"
              color="#50A2A7"
              href="/aboutEn"
            >
              English
            </Typography>
          </Typography>
        </p>
        <font color="#444444">
          <h1> 無意識のメディアとしての空 </h1>
          <iframe
            width="450"
            height="253"
            src="https://www.youtube.com/embed/m2-9UPFok8Q"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen
          />
          <h2 align="left"> About this project </h2>
          <p align="left">
            {" "}
            観光で見知らぬ土地に赴いたときや、災害等の非日常的な状況におかれた時、スマートフォンで得られる情報だけでは不十分なことがあります。この作品では、誰かがその付近でツイートした内容から、その感情を可視化してAR（Augumented
            Reality;
            強化現実）を使って利用者が見ている空に映し出します。これによって、利用者はその地域の空気感を無意識に理解することができるようになります。
          </p>
          <p align="left">
            {" "}
            現在の生活の中ではARは限られた用途でしか利用されていませんが、近い将来、自然な形で常にARを利用する時代がやって来ます。その時の光景の一端を見せることがこの作品の目的です。
          </p>
          <p align="left">
            {" "}
            スマートフォンを使ってアクセスする情報は、意識的に取得することによって得られるものですが、私たちの生活の中には無意識に得られる情報が多数あります。例えば私たちは空から、天気の変化や時間、方角、快適さ等の情報を無意識のうちに得ています。この作品では、利用者が見ている風景の中の空の領域を、無意識でありながら常に利用されるメディアとして置き換えることを提唱します。
          </p>
          <p align="left">
            {" "}
            さらにそこに新たな情報を加えることで、今まで持っていなかった新しい無意識の感覚を身に着けることができると考えます。大気汚染の状況や犯罪発生率等といったものは利用者が通常知覚することができない情報ですが、ARを使って空の色や霞み具合として可視化することで、検知可能にすることができます。また、自分のいる場所の近くで何か事故や災害が起きたとき、近辺でツイートされた情報における感情の変化から即座にそれを検知し、さらに必要に応じて最寄りの避難所の位置が空に示されることで即座な避難行動が可能になります。
          </p>
          <p align="left">
            {" "}
            この様に空は私たちを新しい感覚に導いてくれる巨大なキャンバスになり得るのです。
          </p>
          <br />
          <iframe
            width="450"
            height="253"
            src="https://www.youtube.com/embed/QzdtOkSA72c"
            frameborder="0"
            allow="autoplay; encrypted-media"
            allowfullscreen
          />
          <br />
          <h2 align="left"> 技術的特徴について </h2>
          <p align="left"> 本作品には以下の６つの技術的特徴があります。</p>
          <h3 align="left">
            1) 風景中の空の領域をディープラーニングを使って特定
          </h3>
          <p align="left">
            {" "}
            本作品では、PSPNet（Pyramid Scene Parsing
            Network)と呼ばれるディープラーニングを用いた画像解析技術を採用しています。この技術は2016年に研究機関ImageNetによって主催された風景画像解析競技会において最高精度の技術として認められています。自動運転やロボットセンシング等への応用を想定されたこの技術を本作品においてAR分野で採用したことは新たな試みと言えます。
          </p>
          <h3 align="left">
            {" "}
            2) 画像境界部分の不自然さを緩和する二重球面投影法
          </h3>
          <p align="left">
            {" "}
            上述のPSPNetであっても画像解析の精度には限界があり、時に検出された空の領域は精確でない場合があります。この場合であっても境界部分を自然に見せるために本作品ではVR空間の中で利用者を取り囲む2つの球面に風景を表示させるという手法を提案・実装しました。前面側の球面には空の領域を透明にした画像を用い、後面側には元の風景全体を用いています。利用者は、空に表示される様々な情報をこの２つの面の間から見ることになります。利用者から２つの写像面までの距離が十分であれば利用者からはそれらの間がひと続きに見えるため、境界部分が不正確であっても利用者にとっては自然な風景として見ることができます。
          </p>
          <h3 align="left">
            {" "}
            3)
            視線操作による縮尺制御ユーザインタフェースを具備した上空への地図表示
          </h3>
          <p align="left">
            {" "}
            本作品ではAR空間において地図を確認するための手法として、上空に地図を常時配置するという表現を実現しました。上空に配置することで、風景への干渉を最小限に抑え、常時表示の際に利用者が感じる負担を最小化しています。また、上空の地図が凝視された際に、地図面の高度を変化させることで地図の縮尺変更を行うというユーザインタフェースを提案・実装しました。これにより視線だけで自然に縮尺制御を可能にしています。
          </p>
          <h3 align="left"> 4) 注目点への音源配置</h3>
          <p align="left">
            {" "}
            本作品では効果的に無意識への働きかけを行う方法を追求しています。その方法の一環として、利用者の近傍にある注目すべき場所を知らせために、音源をその注目点に配置しました。利用者は左右の耳に届く音量のバランスの違いから感覚的に注目すべき場所を認識することができます。特に、頭を動かした時に向いている方向に応じて左右の音量のバランスが変化することで、より場所の特定がしやすいようになっています。
          </p>
          <h3 align="left">
            {" "}
            5) 上空に配置された感情表示バーの動きにより情報の鮮度を表現
          </h3>
          <p align="left">
            {" "}
            本作品では上空に表示された情報自体が、オーロラのように美しく、人々に好意を持ってもらえるようになることを目指しました。AR空間内に感情を表現するにあたり、上空に表示するバーの色で感情を表現しただけでなく、感情を計測したツイートの鮮度を、そのバーの動きによって示すようにしています。情報の新しさはバーの動きの活発さや、バーの長さ、上空中の高度によって直感的に理解できるようになっています。
          </p>
          <h3 align="left">
            {" "}
            6)
            上空に表示された巨大な光輪の動きや路面を流れる光の粒子を使った目的地誘導手法
          </h3>
          <p align="left">
            {" "}
            本作品ではポジティブなツイートの集まっている場所や、災害時の避難所の場所等に利用者を誘導する仕組みを設けています。そのためにAR空間の上空に巨大な光輪を表示し、目的地に向かって縮小する動きによって表現することによって、どの方角を利用者が向いていても目的地の方向を意識できるようにしました。また、路面を流れる複数の光の粒子の動きによっても目的地への道筋を示し、群集心理により本能的にその方向に移動したくなるような表現手法を提案・実装しています。
          </p>

          <br />
          <h2 align="left"> About us </h2>
          <p align="left">
            We “STANDY” are a team formed in ASIA OPEN DATA HACKATHON 2017 held
            among four Asian countries and won the top prize there.
          </p>
          <p align="left">
            Members in AODH2018: 　Koichi Okada (JAPAN) Rohit Kumar Singh
            (INDIA) Tang Li Qun (MALAYSIA) Satoshi Yanagisawa (JAPAN)
          </p>
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
