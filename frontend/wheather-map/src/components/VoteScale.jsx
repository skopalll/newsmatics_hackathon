
const computeVotes = (articles) => {
  let leftVotes = 0;
  let rightVotes = 0;
  articles.forEach((article) => {
    const orientation = article[5];
    switch (orientation) {
      case "Right-wing":
        rightVotes += 2;
        break;
      case "Center-right":
        rightVotes += 1;
        break;
      case "Left-wing":
        leftVotes += 2;
        break;
      case "Center-left":
        leftVotes += 1;
        break;
      default:
        break;
    }
  });
  return { leftVotes, rightVotes };
};

export default function VoteScale ({ articles }) {
  const { leftVotes, rightVotes } = computeVotes(articles);
  const totalVotes = leftVotes + rightVotes;
  const leftPercentage = totalVotes ? Math.round((leftVotes / totalVotes) * 100) : 0;
  const rightPercentage = totalVotes ? Math.round((rightVotes / totalVotes) * 100) : 0;

  return (
    <div className="vote-scale" style={{ marginBottom: '1rem' }}>
      <div className="vote-bar" style={{ display: 'flex', height: '20px', overflow: 'hidden', borderRadius: '4px', marginBottom: '0.5rem' }}>
        <div style={{ width: `${leftPercentage || rightPercentage ? leftPercentage : 50}%`, backgroundColor: "#0070C0" }}></div>
        <div style={{ width: `${rightPercentage || leftPercentage ? rightPercentage : 50}%`, backgroundColor: "#BC291E" }}></div>
      </div>
      <div className="vote-text" style={{ textAlign: 'center', fontWeight: 'bold' }}>
        Left: ({leftPercentage || rightPercentage ? leftPercentage : 50}%) | Right: ({rightPercentage || leftPercentage ? rightPercentage : 50}%)
      </div>
    </div>
  );
};