import SearchComponent from "../SearchComponent";
import ItemList from "../ItemList";
import { ImArrowLeft, ImArrowRight } from "react-icons/im";


//redux
import { useSelector } from "react-redux";
import { useState } from "react";

const TopIcons = ({ onClick1 }) => {
  const [leftCol, setLeftCol] = useState("black");

  return (
    <div
      style={{
        height: "35px",
        display: "flex",
        justifyContent: "flex-start",
      }}
    >
      <ImArrowLeft
        size="35"
        color={leftCol}
        onMouseEnter={() => {
          setLeftCol("red");
        }}
        onMouseLeave={() => {
          setLeftCol("black");
        }}
        onClick={onClick1}
        style={{
          cursor: "pointer",
          transition: "all 200ms ease-in-out",
        }}
      />
    </div>
  );
};

// 검색결과 페이지네이션
const PartSelect = ({ setSubProcess }) => {
  const selected = useSelector((state) => {
    return state.recommend.selected;
  });
  const [value, setValue] = useState("");
  const [doSearch, setDoSearch] = useState(false);

  return (
    <div className="partSelect">
      <TopIcons
        onClick1={() => {
          setSubProcess(1);
        }}
      />
      <SearchComponent
        value={value}
        setValue={setValue}
        setDoSearch={setDoSearch}
      />
      <ItemList
        searchValue={value}
        doSearch={doSearch}
        setDoSearch={setDoSearch}
      />
    </div>
  );
};

export default PartSelect;
