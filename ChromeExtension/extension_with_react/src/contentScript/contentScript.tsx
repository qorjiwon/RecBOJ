import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';
import "./MyPage.css";
import "./ProsCons.css";
import ReactTooltip from 'react-tooltip';

function IfSubmitPage() {
    const currentPageURL = window.location.href;
    const desiredURLPattern = "https://www.acmicpc.net/status?from_mine=";
    return currentPageURL.startsWith(desiredURLPattern);
}

function IfMyPage() {
    const currentPageURL = window.location.href;
    const desiredURLPattern = "https://www.acmicpc.net/user/";
    return currentPageURL.startsWith(desiredURLPattern);
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
    problem0_tags: string;
    problem1_tags: string;
    problem2_tags: string;
    problem0_tier: string;
    problem1_tier: string;
    problem2_tier: string;
    message;
}

function RelatedProblem() {
    const [problems, setProblems] = useState<ProblemsType | null>(null);
    useEffect(() => {
        ReactTooltip.rebuild();
    }, []);

    useEffect(() => {
       
        const fetchData = async () => {
            // 모든 #solution-으로 시작하는 요소를 선택
            const elements = document.querySelectorAll("[id^='solution-'] > td.result > span.result-text");

            // 선택한 요소들의 텍스트를 가져옴
            const texts = Array.from(elements).map(element => element.textContent);
            
            // Flask에 URL 전송
            try {
                // 플라스크가 응답할 때까지 await
                const response = await fetch('http://127.0.0.1:8080/send_url', {
                    method: 'POST',
                    body: JSON.stringify({ url: window.location.href, submits: texts }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('서버 응답이 실패했습니다.');
                }
                const data = await response.json();
                const problemsData = typeof data.message === 'string' ? JSON.parse(data.message) : data.message;
                setProblems(problemsData);
            }
            catch (error) {
                console.error('오류 발생: ' + error);
            }
        };

        fetchData();
    }, []);

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
        <div>
        <b>연관 문제 1:</b>
        <a
          data-tip={`유사도: ${problems.problem0_similarity}%, 티어: ${problems.problem0_tier}, 분류: ${problems.problem0_tags}`}
          href={urls.problem0}
          className= 'RecommenedProblem'
        >
          {problems.problem0_titleKo}
        </a>
        &nbsp;
        <b>연관 문제 2:</b>
        <a
          data-tip={` 유사도: ${problems.problem1_similarity}%, 티어: ${problems.problem1_tier}, 분류: ${problems.problem1_tags}`}
          href={urls.problem1}
        >
          {problems.problem1_titleKo}
        </a>
        &nbsp;
        <b>연관 문제 3:</b>
        <a
          data-tip={` 유사도: ${problems.problem2_similarity}%, 티어: ${problems.problem2_tier}, 분류: ${problems.problem2_tags}`}
          href={urls.problem2}
          style={{
            fontWeight: 'bold',
            marginRight: '10px',
            }}
        >
          {problems.problem2_titleKo}
        </a>
        &nbsp;
        <b>&nbsp; {problems.message}</b>
        <ReactTooltip place="top" type="dark" effect="solid"/>
      </div>      
    );
}

if (IfSubmitPage()) {
    const appContainer = document.createElement('div');
    const targetElement = document.querySelector('body > div.wrapper > div.container.content > div.row > div.margin-bottom-30') as HTMLElement;
    if (targetElement) {
        const styles = {
            backgroundColor: '#F5F5F5',
            width: '1143px', // 원하는 너비로 설정
            height: '27px', // 원하는 높이로 설정
            position: 'relative', // 위치 지정을 상대적으로 설정
            left: '13px', // 원하는 오른쪽 이동 거리로 설정
            display: 'flex', // Flexbox 레이아웃 사용
            alignItems: 'center', // 수직 가운데 정렬
            top: '15px' // 원하는 아래로 이동 거리로 설정
        };
        Object.assign(targetElement.style, styles);
    }
    targetElement?.appendChild(appContainer);
    const root = createRoot(appContainer);
    root.render(<RelatedProblem />)
}


function MyPage() {
    const [currentPage, setCurrentPage] = useState(0);
    const [active, setActive] = useState(null);

    const handleClick = (index) => {
        // 현재 클릭한 버튼이 이미 활성 상태라면 비활성 상태로, 그렇지 않다면 활성 상태로 설정
        setCurrentPage((currentPage) => (currentPage === index ? 0 : index));
        setActive((active) => (active === index ? null : index));
    };

    const [selectedField_strong, setSelectedField_strong] = useState<string | null>(null);
    const [selectedButton_strong, setSelectedButton_strong] = useState<string | null>(null);

    const [selectedField_weak, setSelectedField_weak] = useState<string | null>(null);
    const [selectedButton_weak, setSelectedButton_weak] = useState<string | null>(null);

    const handleClick_strong = (field: string) => {
        if (selectedField_strong === field) {
            setSelectedField_strong(null);
            setSelectedButton_strong(null);
        } else {
            setSelectedField_strong(field);
            setSelectedButton_strong(field);
        }
    };


    const handleClick_weak = (field: string) => {
        if (selectedField_weak === field) {
            setSelectedField_weak(null);
            setSelectedButton_weak(null);
        } else {
            setSelectedField_weak(field);
            setSelectedButton_weak(field);
        }
    };

    const CircleComponent = ({ cx, cy, r, fill }) => {
        return <circle cx={cx} cy={cy} r={r} fill={fill} />;
      };

    return (
        <div className="style">
            <div style = {{display: 'flex', borderBottom: '1px solid #ddd'}}>
                <button
                    className={`manu ${active === 1 ? 'active' : ''}`}
                    onClick={() => handleClick(1)}
                >
                    취약 유형 기반 추천
                </button>
                <button
                    className={`manu ${active === 2 ? 'active' : ''}`}
                    onClick={() => handleClick(2)}
                >
                    푼 지 오래된 문제 추천
                </button>
                <button
                    className={`manu ${active === 3 ? 'active' : ''}`}
                    onClick={() => handleClick(3)}
                >
                    유사도 기반 추천
                </button>
            </div>
            <div>
                <div>
                    {currentPage === 1 && (
                    <>
                        <div style={{ display: 'flex', flexDirection: 'column', padding: '10px', margin: '5px' }}>

                            <div style={{display: 'flex', marginBottom: '10px', justifyContent: 'center', alignItems: 'center'}}>

                                <svg style={{ width:"35", height:"35", fill:"none", stroke:"#8a8f95", strokeWidth:"2"}} viewBox="0 0 35 35">
                                    <g transform="translate(8, 10)">
                                        <CircleComponent cx="8.5" cy="8.5" r="1" fill="currentColor" />
                                        <path d="M4 7v3.859c0 .537 .213 1.052 .593 1.432l8.116 8.116a2.025 2.025 0 0 0 2.864 0l4.834 -4.834a2.025 2.025 0 0 0 0 -2.864l-8.117 -8.116a2.025 2.025 0 0 0 -1.431 -.593h-3.859a3 3 0 0 0 -3 3z"></path>
                                    </g>
                                </svg>
                                <button
                                    className={`tagbtn_weak${selectedButton_weak === 'greedy' ? ' active' : ''}`}
                                    onClick={() => handleClick_weak('greedy')}
                                    >
                                    Greedy
                                </button>
                                <svg style={{ width:"35", height:"35", fill:"none", stroke:"#8a8f95", strokeWidth:"2"}} viewBox="0 0 35 35">
                                    <g transform="translate(8, 10)">
                                        <CircleComponent cx="8.5" cy="8.5" r="1" fill="currentColor" />
                                        <path d="M4 7v3.859c0 .537 .213 1.052 .593 1.432l8.116 8.116a2.025 2.025 0 0 0 2.864 0l4.834 -4.834a2.025 2.025 0 0 0 0 -2.864l-8.117 -8.116a2.025 2.025 0 0 0 -1.431 -.593h-3.859a3 3 0 0 0 -3 3z"></path>
                                    </g>
                                </svg>
                                <button
                                    className={`tagbtn_weak${selectedButton_weak === 'dac' ? ' active' : ''}`}
                                    onClick={() => handleClick_weak('dac')}
                                    >
                                    Divide and Conquer
                                </button>
                                <svg style={{ width:"35", height:"35", fill:"none", stroke:"#8a8f95", strokeWidth:"2"}} viewBox="0 0 35 35">
                                    <g transform="translate(8, 10)">
                                        <CircleComponent cx="8.5" cy="8.5" r="1" fill="currentColor" />
                                        <path d="M4 7v3.859c0 .537 .213 1.052 .593 1.432l8.116 8.116a2.025 2.025 0 0 0 2.864 0l4.834 -4.834a2.025 2.025 0 0 0 0 -2.864l-8.117 -8.116a2.025 2.025 0 0 0 -1.431 -.593h-3.859a3 3 0 0 0 -3 3z"></path>
                                    </g>
                                </svg>
                                <button
                                    className={`tagbtn_weak${selectedButton_weak === 'ds' ? ' active' : ''}`}
                                    onClick={() => handleClick_weak('ds')}
                                    >
                                    Data Structure
                                </button>
                                <div className="qmark">
                                    <path d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"></path>
                                </div>
        
                                </div>
                                {selectedField_weak && (
                                    <div className="container_rp" style = {{display: 'flex', flexDirection: 'row'}}>
                                        {problems[selectedField_weak]?.map((problem, index) => (
                                            <div className='rp_all' style = {{display: 'flex', flexDirection: 'column'}}>
                                                <div className='pBox_header'>
                                                    <a href={`/${selectedField_weak}/${problem}`} className="link">
                                                    {problem}
                                                    </a>
                                                </div>
                                                <div className='pBox_content'>
                                                </div>
                                            </div>
                                            ))}
                                    </div>
                                )}
                            </div>
                    </>
                    )}
                    {currentPage === 2 && (
                        <>
                        <div style={{fontSize: '23px', fontFamily: 'Arial, sans-serif', marginBottom: '2px', textAlign: 'center', marginTop: '13px', color: '#6D7856'}}>
                            해당 분류의 문제를 푼 지 오래됐어요.
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                            <div className='divStyle'>
                                <div className='Box' id = 'Box1'>
                                    <div className = 'pBox' id = "Problem1">
                                    <a 
                                        data-tip = {`난이도: Gold4, 분류: backtracking, bruteforcing`}
                                        className = 'hrefBox' href='https://www.acmicpc.net/problem/9663'>
                                             N-Queen </a>
                                    </div>
                                    <div className = 'eBox' id = "explanation1">
                                        현재 backtracking 내용을 42.5% 기억하고 있어요.
                                        <br></br>내일은 38.7% 기억할 거예요.
                                    </div>
                                </div>
                                <div className='Box' id = 'Box2'>
                                    <div className = 'pBox' id = "Problem2">
                                        <a 
                                        className = 'hrefBox' href='https://www.acmicpc.net/problem/1977'
                                        data-tip = {`난이도: Bronze4, 분류: math, implementation, bruteforcing`}
                                        >
                                         완전 제곱수 </a>
                                    </div>
                                    <div className = 'eBox' id = "explanation2">
                                    현재 implementation 분야를 34.7% 기억하고 있어요.
                                    <br></br>내일은 32.8% 기억할 거예요.
                                    </div>
                                </div>
                                <div className='Box' id = 'Box3'>
                                    <div className = 'pBox' id = "Problem3">
                                        <a 
                                            data-tip = {`난이도: Gold5, 분류: math, implementation, bruteforcing`}
                                            className = 'hrefBox'
                                            href='https://www.acmicpc.net/problem/1759'>
                                             암호만들기 </a>
                                    </div>
                                    <div className = 'eBox' id = "explanation3">
                                        현재 brute_forcing 분야를 23.2% 기억하고 있어요.
                                        <br></br>내일은 22.4% 기억할 거예요.
                                    </div>
                                </div>
                            </div>
                            <div style={{ textAlign: 'right', fontSize: '13px', paddingRight: '3%' }}>
                                 <a style={{color: 'black', fontWeight: 'bold'}} href='https://ko.wikipedia.org/wiki/%EB%A7%9D%EA%B0%81_%EA%B3%A1%EC%84%A0'>에빙하우스의 망각곡선이란?</a>
                            </div>
                            <ReactTooltip place="top" type="success" effect="solid"/>
                        </div>
                        </>
                    )}
                    {currentPage === 3 && (
                        <>
                        <div style={{fontSize: '24px', fontFamily: 'Arial, sans-serif', margin: 'auto', textAlign: 'center', marginTop: '13px', color: '#6D7856'}}>
                                이런 문제는 어떤가요?
                            </div>
                            <div className='divStyle'>
                                <div className='Box' id = 'Box1'>
                                    <div className = 'pBox' id = "Problem1">
                                        추천 문제 1번
                                    </div>
                                    <div className = 'eBox' id = "explanation1">
                                        추천 이유 등 메세지
                                    </div>
                                </div>
                                <div className='Box' id = 'Box2'>
                                    <div className = 'pBox' id = "Problem2">
                                        추천 문제 2번
                                    </div>
                                    <div className = 'eBox' id = "explanation2">
                                        추천 이유 등 메세지
                                    </div>
                                </div>
                                <div className='Box' id = 'Box3'>
                                    <div className = 'pBox' id = "Problem3">
                                        추천 문제 3번
                                    </div>
                                    <div className = 'eBox' id = "explanation3">
                                        추천 이유 등 메세지
                                    </div>
                                </div>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

interface tagsType {
    strong0: string;
    strong1: string;
    strong2: string;
    weak0: string;
    weak1: string;
    weak2: string;
}

const problems = {
    dp: ['피보나치 수열', 'KnapSack', '1로 만들기'],
    graph: ['문제 4', '문제 5', '문제 6'],
    string: ['문제 7', '문제 8', '문제 9'],
    dac: ['문제 10', '문제 11', '문제 12'],
    ds : ['문제 13', '문제 14', '문제 15'],
    greedy: ['수 묶기', '선 긋기', '공주님의 정원']
};

const details = {
    dp: ['피보나치 수열', 'KnapSack', '1로 만들기'],
    graph: ['문제 4', '문제 5', '문제 6'],
    string: ['문제 7', '문제 8', '문제 9'],
    dac: ['문제 10', '문제 11', '문제 12'],
    ds : ['문제 13', '문제 14', '문제 15'],
    greedy: ['수 묶기', '선 긋기', '공주님의 정원']
}

function ProsCons() {
    const [tags, setTags] = useState<tagsType | null>(null);
    
    const [selectedField_strong, setSelectedField_strong] = useState<string | null>(null);
    const [selectedButton_strong, setSelectedButton_strong] = useState<string | null>(null);

    const [selectedField_weak, setSelectedField_weak] = useState<string | null>(null);
    const [selectedButton_weak, setSelectedButton_weak] = useState<string | null>(null);

    const handleClick_strong = (field: string) => {
        if (selectedField_strong === field) {
            setSelectedField_strong(null);
            setSelectedButton_strong(null);
        } else {
            setSelectedField_strong(field);
            setSelectedButton_strong(field);
        }
    };


    const handleClick_weak = (field: string) => {
        if (selectedField_weak === field) {
            setSelectedField_weak(null);
            setSelectedButton_weak(null);
        } else {
            setSelectedField_weak(field);
            setSelectedButton_weak(field);
        }
    };
    useEffect(() => {
       
        const fetchTags = async () => {
        
                const response = await fetch('http://127.0.0.1:8080/tags', {
                    method: 'POST',
                    body: JSON.stringify({ url: window.location.href}),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('서버 응답이 실패했습니다.');
                }
                const data = await response.json();
                let tagsData;
                try {
                    tagsData = JSON.parse(data.message);
                } catch (error) {
                    tagsData = data.message;
                }

                setTags(tagsData);
        };

        fetchTags();
    }, []);

    const CircleComponent = ({ cx, cy, r, fill }) => {
        return <circle cx={cx} cy={cy} r={r} fill={fill} />;
      };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', padding: '10px', margin: '5px' }}>
        <div style={{ borderBottom: '0.7px solid #7f8c8d', padding: '10px', marginBottom: '10px', }}>
            <b style={{ fontSize: '14px' }}>강점 분야:</b>
            <svg style={{ width:"35", height:"35", fill:"none", stroke:"#8a8f95", strokeWidth:"2"}} viewBox="0 0 35 35">
                <g transform="translate(8, 10)">
                    <CircleComponent cx="8.5" cy="8.5" r="1" fill="currentColor" />
                    <path d="M4 7v3.859c0 .537 .213 1.052 .593 1.432l8.116 8.116a2.025 2.025 0 0 0 2.864 0l4.834 -4.834a2.025 2.025 0 0 0 0 -2.864l-8.117 -8.116a2.025 2.025 0 0 0 -1.431 -.593h-3.859a3 3 0 0 0 -3 3z"></path>
                </g>
            </svg>
            <button
                className={`tagbtn${selectedButton_strong === 'dp' ? ' active' : ''}`}
                onClick={() => handleClick_strong('dp')}
                >
                DP
            </button>
            <svg style={{ width:"35", height:"35", fill:"none", stroke:"#8a8f95", strokeWidth:"2"}} viewBox="0 0 35 35">
                <g transform="translate(8, 10)">
                    <CircleComponent cx="8.5" cy="8.5" r="1" fill="currentColor" />
                    <path d="M4 7v3.859c0 .537 .213 1.052 .593 1.432l8.116 8.116a2.025 2.025 0 0 0 2.864 0l4.834 -4.834a2.025 2.025 0 0 0 0 -2.864l-8.117 -8.116a2.025 2.025 0 0 0 -1.431 -.593h-3.859a3 3 0 0 0 -3 3z"></path>
                </g>
            </svg>
            <button
                className={`tagbtn${selectedButton_strong === 'graph' ? ' active' : ''}`}
                onClick={() => handleClick_strong('graph')}
                >
                Graph
            </button>
            <svg style={{ width:"35", height:"35", fill:"none", stroke:"#8a8f95", strokeWidth:"2"}} viewBox="0 0 35 35">
                <g transform="translate(8, 10)">
                    <CircleComponent cx="8.5" cy="8.5" r="1" fill="currentColor" />
                    <path d="M4 7v3.859c0 .537 .213 1.052 .593 1.432l8.116 8.116a2.025 2.025 0 0 0 2.864 0l4.834 -4.834a2.025 2.025 0 0 0 0 -2.864l-8.117 -8.116a2.025 2.025 0 0 0 -1.431 -.593h-3.859a3 3 0 0 0 -3 3z"></path>
                </g>
            </svg>
            <button
                className={`tagbtn${selectedButton_strong === 'greedy' ? ' active' : ''}`}
                onClick={() => handleClick_strong('greedy')}
                >
                Greedy
            </button>
        </div>
        {selectedField_strong && (
                  <div className="container_rp">
                  <h2 className="header_rp">{`${selectedField_strong} 관련 문제`}</h2>
                  <ul className="list_rp">
                    {problems[selectedField_strong]?.map((problem, index) => (
                      <li key={index} className="listItem">
                        <a
                          href={`/${selectedField_strong}/${problem}`}
                          className={`link ${problem === 'KnapSack' ? 'correctColor' : ''}`}
                        >
                          {problem}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>                
                  )}      
        </div>
    );
};



if (IfMyPage()) {
    const targetSelector = "body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div > div.col-md-9 > div:nth-child(1) > div.panel-body";
    const targetElement = document.querySelector(targetSelector);
    
    const parentElement = targetElement.parentElement;
    
    // 새로운 divElement를 생성하여 첫 번째 root를 생성합니다.
    const divElement1 = document.createElement("div");
    parentElement.appendChild(divElement1);
    const root1 = createRoot(divElement1);
    root1.render(<ProsCons />);
    
    // 새로운 divElement를 생성하여 두 번째 root를 생성합니다.
    const divElement2 = document.createElement("div");
    parentElement.appendChild(divElement2);
    const root2 = createRoot(divElement2);
    root2.render(<MyPage />);
}