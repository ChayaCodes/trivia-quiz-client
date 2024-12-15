import React from 'react';
import './GamesPage.css';
import FlipBox from '../../components/FlipBox/FlipBox';
import FrontCard from '../../components/FrontCard/FrontCard';
import UnderConstruction from '../../components/UnderConstruction/UnderConstruction';
import angryBirdsGif from '../../assets/images/pg11.gif';
import ticTacToeGif from '../../assets/images/pg9.gif';
import mazeGif from '../../assets/images/gip.gif';
import tetrisGif from '../../assets/images/pg10.gif';
import bullseyeGif from '../../assets/images/giphy1.gif';
import ticTacToeGif2 from '../../assets/images/pg6.gif';
import monopolyGif from '../../assets/images/pg7.gif';
import marioGif from '../../assets/images/pg8.gif';
import Logo from '../../components/Logo/Logo';
import "./../blackStyle.css";


const GamesPage = ({name = ""}) => {
  return (
    <div className="bodyGames">
      <div className="rmhv">
        <h2 className="toname"> שלום {name} </h2>
        <h1>מה תרצו לשחק היום?</h1>
      </div>
      <Logo />
      <div className="games">
        <FlipBox
          front={<FrontCard image={ticTacToeGif2} name="פקמן" />}
          back={<UnderConstruction />}
        />
        <FlipBox
          front={<FrontCard image={angryBirdsGif} name="angry birds" />}
          back={<UnderConstruction />}
        />
        <FlipBox
          front={<FrontCard image={bullseyeGif} name="בול פגיעה" />}
          back={<UnderConstruction />}
        />
        <FlipBox
          front={<FrontCard image={monopolyGif} name="מונפול" />}
          back={<UnderConstruction />}
        />
        <FlipBox
          front={<FrontCard image={marioGif} name="מריו" />}
          back={<UnderConstruction />}
        />
        <FlipBox
          front={<FrontCard image={ticTacToeGif} name="איקס עיגול" />}
          back={<UnderConstruction />}
        />
        <FlipBox
          front={<FrontCard image={tetrisGif} name="טטריס" />}
          back={<UnderConstruction />}
        />
        <FlipBox
          front={<FrontCard image={mazeGif} name="מבוך" />}
          back={<UnderConstruction />}
        />
      </div>
    </div>
  );
};

export default GamesPage;