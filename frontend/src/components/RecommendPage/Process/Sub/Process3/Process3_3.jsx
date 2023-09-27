const Item = ({ imgUrl, value }) => {
  const onClick = () => {};

  return (
    <div className="item" onClick={onClick}>
      <div
        className="item-top"
        style={{
          backgroundImage: `url(${imgUrl})`,
        }}
      ></div>
      <div className="item-bot">{value}</div>
    </div>
  );
};

// 소분류에 해당하는 것2
// 컴포넌트만 존재
// 컴포넌트 재사용 기존에 존재하던 것
const Process3_3 = ({ setSubProcess }) => {
  return <></>;
};

export default Process3_3;
