
import AnswerGroup from "./AnswerGroup";

const AnswerGroupList = ({ groups }) => {

    return (
        <div className="answergroup-list">
        <ul>
        {groups.map(group => (
            <li key={group.id}>
                <AnswerGroup answerGroup={group} onGroupModified={() => {}} />
            </li>
        ))}
        </ul>
        </div>
    );
}

export default AnswerGroupList;
