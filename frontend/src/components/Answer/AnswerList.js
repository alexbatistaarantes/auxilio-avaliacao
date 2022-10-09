import SelectionTool from '../SelectionTool';

import Answer from './Answer';

const AnswerList = ({answers, selectAnswer, allowModification=true, onAnswerModified}) => {

    return (
        <div className="answers region-list">
            <ul>
            {answers.map((answer) => (
                <li key={ answer.id }>
                    <Answer answer={answer} allowModification={allowModification} onAnswerModified={() => onAnswerModified()}/>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default AnswerList;
