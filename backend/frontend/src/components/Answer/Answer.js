import { useState } from "react";

import { getCookie } from "../../utils/cookie";
import SelectionTool from "../SelectionTool";

const Answer = ({
    answer, 
    answerTitle=null, // null, label, studentId
    
    allowSelection=false, // permite selecionar respostas com checkbox
    onAnswerSelected, // callback quando alguma resposta for selecionada
    onAnswerUnselected, // callback quando alguma resposta for deselecionada

    allowModification=true, // permite editar região
    onAnswerModified, // callback quando região modificada

    showImage=true // mostrar ou não imagem da resposta
}) => {

    const [ checked, setChecked ] = useState(false);
    const [ toggleModification, setToggleModification ] = useState(false);
    const [ cropRegion, setCropRegion ] = useState({
        unit: '%',
        x: (answer.x / answer.submission_width) * 100,
        y: (answer.y / answer.submission_height) * 100,
        width: (answer.width / answer.submission_width) * 100,
        height: (answer.height / answer.submission_height) * 100,
    });
    const [ propagate, setPropagate ] = useState(true);
    
    const saveModification = () => {

        const body = {
            id: answer.id,
            x: parseInt((cropRegion.x / 100) * answer.submission_width),
            y: parseInt((cropRegion.y / 100) * answer.submission_height),
            width: parseInt((cropRegion.width / 100) * answer.submission_width),
            height: parseInt((cropRegion.height / 100) * answer.submission_height),

            modified: true,
            propagate: propagate
        };

        const csrftoken = getCookie('csrfToken');

        fetch(`/api/answers/${answer.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(body)
        }).then(() => {
            onAnswerModified();
            setToggleModification(false);
        });
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        const points = event.target.points.value;
        const feedback = event.target.feedback.value;

        const csrfToken = getCookie('csrfToken');

        fetch(`/api/answers/${answer.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                points: points,
                feedback: feedback
            })
        }).then(() => {
            onAnswerModified();
        })
    }

    return (
        <div className="answer">
            {/* Caixa de Seleção */}
            {allowSelection && 
            <input
                checked={checked}
                onChange={() => {
                    if(!checked) onAnswerSelected(answer.id)
                    else onAnswerUnselected(answer.id);
                    setChecked(!checked);
                }}
                type="checkbox" 
            />
            }

            {/* Título da resposta (nenhum, label do campo ou identificador do aluno) */}
            { answerTitle !== null &&
            <h2>
                { answerTitle === 'label' && answer.field_label }
                { answerTitle === 'studentId' && answer.studentId }
            </h2>
            }

            {/* Imagem da resposta */}
            { showImage && <img className="region-image" src={ answer.image } alt="" />}
            
            {/*  */}
            <form onSubmit={(event) => handleSubmit(event)}>
                <input name="points" id="points" type="number" step="0.01"
                    defaultValue={answer.points}
                    min={0} max={answer.field_points}
                    placeholder="Nota"
                    disabled={answer.group_name && true}
                /> / {answer.field_points}
                <textarea name="feedback" id="feedback"
                    defaultValue={answer.feedback}
                    placeholder="Comentário" cols="30" rows="1"
                    disabled={answer.group_name && true}
                ></textarea>
                
                {!answer.group_name && <input type="submit" value="Salvar nota" />}
            </form>

            {allowModification &&
            <div>
                <button onClick={() => setToggleModification(!toggleModification)}>
                    {!toggleModification && ("Editar")}
                    {toggleModification && ("Cancelar edição")}
                </button>
                { toggleModification && (
                <div>
                    <button onClick={() => saveModification()}> Salvar edição </button>

                    <div>
                        <label htmlFor="propagate-modification">Propagar edição para outras respostas?</label>
                        <input checked={propagate} onChange={() => propagate ? setPropagate(false) : setPropagate(true)} type="checkbox" name="propagate-modification" id="propagate-modification" />
                    </div>

                    <SelectionTool
                        src={answer.submission_image}
                        crop={cropRegion}
                        onCropChange={(c) => setCropRegion(c)}
                    />
                </div>
                )}
            </div>
            }
            
            
        </div>
    );
}

export default Answer;
