import SelectionTool from '../SelectionTool';

import Answer from './Answer';

const AnswerList = ({answers, groupedBy, allowModification=true, onAnswerModified}) => {

    return (
        <div className="answers region-list">
            <ul>
            {answers.map((answer) => (
                <li key={ answer.id }>
                    <Answer answer={answer} answerTitle={groupedBy} allowModification={allowModification} onAnswerModified={() => onAnswerModified()}/>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default AnswerList;
