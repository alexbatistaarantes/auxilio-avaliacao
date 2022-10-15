import SelectionTool from '../SelectionTool';

import Answer from './Answer';

const AnswerList = ({
    answers, 
    answerTitle, // null, label, studentId
    
    allowSelection=false, // permite selecionar respostas com checkbox
    onAnswerSelected, // callback quando alguma resposta for selecionada
    onAnswerUnselected,

    allowModification=true, // permite editar região
    onAnswerModified // callback quando região modificada
}) => {

    return (
        <div className="answers region-list">
            <ul>
            {answers.map((answer) => (
                <li key={ answer.id }>
                    <Answer 
                        answer={answer}
                        answerTitle={answerTitle}
                        
                        allowSelection={allowSelection}
                        onAnswerSelected={onAnswerSelected}
                        onAnswerUnselected={onAnswerUnselected}

                        allowModification={allowModification} 
                        onAnswerModified={onAnswerModified}
                    />
                </li>
            ))}
            </ul>
        </div>
    );
}

export default AnswerList;
