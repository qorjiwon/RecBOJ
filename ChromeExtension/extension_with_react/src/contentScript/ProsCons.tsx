import React, { useState, useEffect } from 'react';
import './style/ProsCons.css'

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
    graph: ['DFS와 BFS', '미로 탐색', '바이러스'],
    greedy: ['Contact', '명령 프롬프트', '36진수'],
};

function ProsCons() {
    const [tags, setTags] = useState<tagsType | null>(null);
    const [selectedField_strong, setSelectedField_strong] = useState<string | null>(null);
    const [selectedButton_strong, setSelectedButton_strong] = useState<string | null>(null);
 
    const handleClick_strong = (field: string) => {
        if (selectedField_strong === field) {
            setSelectedField_strong(null);
            setSelectedButton_strong(null);
        } else {
            setSelectedField_strong(field);
            setSelectedButton_strong(field);
        }
    };

    useEffect(() => {
       
        const fetchTags = async () => {
        
                const response = await fetch('http://127.0.0.1:8000/tags', {
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
                  <ul style={{display: 'flex', flexDirection: 'column'}} className="list_rp">
                    {problems[selectedField_strong]?.map((problem, index) => (
                      
                      <div key={index} className="listItem">
                        <a
                          href={`/${selectedField_strong}/${problem}`}
                          className={`link ${problem === 'KnapSack' ? 'correctColor' : ''}`}
                        >
                          {problem}
                        </a>
                      </div>
                    ))}
                  </ul>
                </div>                
                  )}      
        </div>
    );
};

export default ProsCons;