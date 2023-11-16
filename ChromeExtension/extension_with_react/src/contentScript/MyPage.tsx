import React, { useState} from 'react';
import "./MyPage.css";
import ReactTooltip from 'react-tooltip';


const problems = {
    dp: ['피보나치 수열', 'KnapSack', '1로 만들기'],
    graph: ['문제 4', '문제 5', '문제 6'],
    string: ['문제 7', '문제 8', '문제 9'],
    dac: ['문제 10', '문제 11', '문제 12'],
    ds : ['문제 13', '문제 14', '문제 15'],
    greedy: ['문제 16', '문제 17', '문제 18']
};
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


export default MyPage;