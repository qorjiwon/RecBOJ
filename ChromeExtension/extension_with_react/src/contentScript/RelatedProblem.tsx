import React, { useState, useEffect, useRef } from 'react';
import ReactTooltip from 'react-tooltip';
import './style/RelatedProblem.css' 

function RelatedProblem() {
    const [problems, setProblems] = useState<ProblemsType | null>(null);
    const [rotate, setRotate] = useState(0);

    useEffect(() => {
        ReactTooltip.rebuild();
    }, []);

    const handleRotate = () =>
    {
      setRotate(rotate => rotate + 1);
    }
    useEffect(() => {
       
        const fetchData = async () => {

            console.log(rotate);
            // 모든 #solution-으로 시작하는 요소를 선택
            const elements = document.querySelectorAll("[id^='solution-'] > td.result > span.result-text");

            // 선택한 요소들의 텍스트를 가져옴
            const texts = Array.from(elements).map(element => element.textContent);
            
            // Flask에 URL 전송
            try {
                // https://recproblem.site
                const response = await fetch('http://127.0.0.1:8000/submit_page/', {
                    method: 'POST',
                    body: JSON.stringify({ url: window.location.href, submits: texts, div: rotate }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('서버 응답이 실패했습니다.');
                }
                const data = await response.json();
                
                setProblems(data);
                
                
            }
            catch (error) {
                console.error('오류 발생: ' + error);
            }

        };
        fetchData();
    }, [rotate]);

    console.log(problems);
    const urls: Record<string, string> = {};
    const problem_ids: Record<string, string> = {};
    
    if (problems) {
        for (let i = 0; i < 3; i++) { // problem0, problem1, problem2에 대해서만 반복
            const key = `problem${i}` as keyof ProblemsType;
            const problemNumber = problems[key];
            const url = `https://www.acmicpc.net/problem/${problemNumber}`;
            urls[key] = url;
            problem_ids[key] = problemNumber;
        }
    }

    console.log("URL_problem0 =", urls.problem0);
    console.log("URL_problem1 =", urls.problem1);
    console.log("URL_problem2 =", urls.problem2);
    console.log(problems)
    if (!problems) {
        return null;
    }
    return (
      <div key={rotate} className='ContainerToRender'>
              <div style={{width: '96%', display: 'flex', flexDirection: 'row'}}>
                <div className='problem_container' >
                    <b className='problem_index'>연관 문제 1: </b>
                    <a
                      data-tip={`유사도: ${problems.problem0_similarity}%, 티어: ${problems.problem0_tier}, 분류: ${problems.problem0_tags}`}
                      href={urls.problem0}
                      className= 'RecommenedProblem'
                    >
                      {problems.problem0_titleKo}
                    </a>
                </div>
                <div className='problem_container'>
                    <b className='problem_index'>연관 문제 2: </b>
                    <a
                      data-tip={` 유사도: ${problems.problem1_similarity}%, 티어: ${problems.problem1_tier}, 분류: ${problems.problem1_tags}`}
                      href={urls.problem1}
                      className= 'RecommenedProblem'
                    >
                      {problems.problem1_titleKo}
                    </a>
                </div>
                <div className='problem_container'>
                    <b className='problem_index' >연관 문제 3: </b>
                    <a
                      data-tip={` 유사도: ${problems.problem2_similarity}%, 티어: ${problems.problem2_tier}, 분류: ${problems.problem2_tags}`}
                      href={urls.problem2}
                      className= 'RecommenedProblem'
                      style={{
                        marginRight: '10px',
                        }}
                    >
                      {problems.problem2_titleKo}
                    </a>
                </div>
                <b className='message'>{problems.message}</b>
              </div>
          <ReactTooltip place="top" type="dark" effect="solid"/>
          <div style={{ width: '4%', display: 'flex', justifyContent: 'right'}}>
              <button className='reloading' onClick={() => handleRotate()}></button>
          </div>
      </div>      
  );
}





interface ProblemsType {
  problem0: string;
  problem1: string;
  problem2: string;
  problem0_similarity: string;
  problem1_similarity: string;
  problem2_similarity: string;
  problem0_titleKo: string;
  problem1_titleKo: string;
  problem2_titleKo: string;
  problem0_tags: string[];
  problem1_tags: string[];
  problem2_tags: string[];
  problem0_tier: string;
  problem1_tier: string;
  problem2_tier: string;
  message;
}


export default RelatedProblem;
