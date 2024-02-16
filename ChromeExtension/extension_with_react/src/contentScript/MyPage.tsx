import React, { useState, useEffect} from 'react';
import "./style/MyPage.css";
import ReactTooltip from 'react-tooltip';
import { CSSTransition } from 'react-transition-group';

function MyPage() {
      const [problems, setRes] = useState<ResponseData | null>(null);
      const [currentPage, setCurrentPage] = useState(0);
      const [active, setActive] = useState(null);
      const [selectedField_weak, setSelectedField_weak] = useState<string | null>('tag1');
      const [selectedButton_weak, setSelectedButton_weak] = useState<string | null>('tag1');
      const [rotate, setRotate] = useState(0);
      const [isOptionsVisible, setOptionsVisible] = useState(false);
      const [filterTier, setFilter] = useState('None');

      useEffect(() => {
         
          const fetchData = async () => {
            console.log("Inside fetchData function");
       
              try {
                const requestData: MyPageRequest = {
                    url: window.location.href,
                    div: rotate,
                    filter: filterTier,
                  };
            
                  // https://recproblem.site
                  const response = await fetch('http://127.0.0.1:8000/mypage/problems', {
                      method: 'POST',
                      body: JSON.stringify(requestData),
                      headers: {
                          'Content-Type': 'application/json'
                      },
                  });
  
                  if (!response.ok) {
                      throw new Error('서버 응답이 실패했습니다.');
                  }
                  const data = await response.json();
                  setRes(data);
              }
              catch (error) {
                if (error.respons) {
                    // 유효성 검사 오류 발생 시
                    const errorData = await error.response.json();
                    console.error("detail: ",errorData.detail);
                  } else {
                    console.error('에러 발생:', error);
                  }
              }
          };
  
          fetchData();
      }, [rotate]);
      console.log(problems);
      
    useEffect(() => {
        ReactTooltip.rebuild();
    }, []);


    const toggleOptions = () => {
        setOptionsVisible(!isOptionsVisible);
      };
  
     const handleFilter = (tier) => {
        setFilter(tier);
        handleRotate();
        toggleOptions();
        console.log(filterTier);
        console.log(rotate)    
     }

    const handleClick = (index) => {
        // 현재 클릭한 버튼이 이미 활성 상태라면 비활성 상태로, 그렇지 않다면 활성 상태로 설정
        setCurrentPage((currentPage) => (currentPage === index ? 0 : index));
        setActive((active) => (active === index ? null : index));
    };


    const handleClick_weak = (field: string) => {
        if (selectedField_weak === field) {
            setSelectedField_weak(null);
            setSelectedButton_weak(null);
        } else {
            console.log(field)
            setSelectedField_weak(field);
            setSelectedButton_weak(field);
        }
    };

    const CircleComponent = ({ cx, cy, r, fill }) => {
        return <circle cx={cx} cy={cy} r={r} fill={fill} />;
      };

    // 클릭 이벤트 핸들러
    const contentClick = (url) => {
        // 동적으로 생성된 URL을 사용하려면 여기에서 로직을 추가
        const dynamicURL = url; // 동적으로 생성된 URL

        // 지정된 URL로 이동
        window.location.href = dynamicURL;
    };
    
   
    const handleRotate = () =>
    {
      setRotate(rotate => rotate + 1);
    }

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
                    실력 기반 추천
                </button>
            </div>
            <div>
                <div style = {{marginTop : '13px'}}>
                    {currentPage === 1 && (
                    <>
                        <div key={rotate} style={{ display: 'flex', flexDirection: 'column'}}>
                            
                            <div style={{display: 'flex', marginBottom: '10px', justifyContent: 'center', alignItems: 'center'}}>
                                
                                <svg style={{ width:"35", height:"35", fill:"none", stroke:"#8a8f95", strokeWidth:"2"}} viewBox="0 0 35 35">
                                    <g transform="translate(8, 10)">
                                        <CircleComponent cx="8.5" cy="8.5" r="1" fill="currentColor" />
                                        <path d="M4 7v3.859c0 .537 .213 1.052 .593 1.432l8.116 8.116a2.025 2.025 0 0 0 2.864 0l4.834 -4.834a2.025 2.025 0 0 0 0 -2.864l-8.117 -8.116a2.025 2.025 0 0 0 -1.431 -.593h-3.859a3 3 0 0 0 -3 3z"></path>
                                    </g>
                                </svg>
                                <button
                                    className={`tagbtn_weak${selectedButton_weak === 'tag1' ? ' active' : ''}`}
                                    onClick={() => handleClick_weak('tag1')}
                                    >
                                    {problems.weak_tag_problems.tag1.tag_name}
                                </button>
                                <svg style={{ width:"35", height:"35", fill:"none", stroke:"#8a8f95", strokeWidth:"2"}} viewBox="0 0 35 35">
                                    <g transform="translate(8, 10)">
                                        <CircleComponent cx="8.5" cy="8.5" r="1" fill="currentColor" />
                                        <path d="M4 7v3.859c0 .537 .213 1.052 .593 1.432l8.116 8.116a2.025 2.025 0 0 0 2.864 0l4.834 -4.834a2.025 2.025 0 0 0 0 -2.864l-8.117 -8.116a2.025 2.025 0 0 0 -1.431 -.593h-3.859a3 3 0 0 0 -3 3z"></path>
                                    </g>
                                </svg>
                                <button
                                    className={`tagbtn_weak${selectedButton_weak === 'tag2' ? ' active' : ''}`}
                                    onClick={() => handleClick_weak('tag2')}
                                    >
                                    {problems.weak_tag_problems.tag2.tag_name}
                                </button>
                                <svg style={{ width:"35", height:"35", fill:"none", stroke:"#8a8f95", strokeWidth:"2"}} viewBox="0 0 35 35">
                                    <g transform="translate(8, 10)">
                                        <CircleComponent cx="8.5" cy="8.5" r="1" fill="currentColor" />
                                        <path d="M4 7v3.859c0 .537 .213 1.052 .593 1.432l8.116 8.116a2.025 2.025 0 0 0 2.864 0l4.834 -4.834a2.025 2.025 0 0 0 0 -2.864l-8.117 -8.116a2.025 2.025 0 0 0 -1.431 -.593h-3.859a3 3 0 0 0 -3 3z"></path>
                                    </g>
                                </svg>
                                <button
                                    className={`tagbtn_weak${selectedButton_weak ===  'tag3' ? ' active' : ''}`}
                                    onClick={() => handleClick_weak('tag3')}
                                    >
                                    {problems.weak_tag_problems.tag3.tag_name}
                                </button>
                                
                            </div>
                                {selectedField_weak && (
                                    <div>
                                        <div className='weak_message'>{problems.weak_tag_problems[selectedField_weak].weak_pcr}%만큼 약한 분야에요</div>
                                        <div style={{display: 'flex', alignItems: 'center'}}>
                                            <button className='reloadingM' onClick={() => handleRotate()}></button>
                                            <div className="option-button-container">
                                                <button className="toggleOptions" onClick={toggleOptions} > 난이도 필터 </button>
                                                <CSSTransition
                                                    in={isOptionsVisible}
                                                    timeout={250}
                                                    classNames="options"
                                                    unmountOnExit
                                                >
                                                    <div className="options">
                                                        <button onClick={() => handleFilter('None')}>무작위</button>
                                                        <button onClick={() => handleFilter('Silver')}>실버</button>
                                                        <button onClick={() => handleFilter('Gold')}>골드</button>
                                                        <button onClick={() => handleFilter('Platinum')}>플래티넘</button>
                                                        <button onClick={() => handleFilter('Diamond')}>다이아몬드</button>
                                                    </div>
                                                </CSSTransition>
                                            </div>
                                        </div>
                                    <div className="container_rp" >
                                            {problems.weak_tag_problems[selectedField_weak].problems ?.map((problem, index) => (
                                                <div className='rp_all'>   
                                                    <button 
                                                    className='pBox_content'
                                                    data-tip={`${problem}번 풀러 가기`}
                                                    onClick={() => contentClick(`https://www.acmicpc.net/problem/${problem}`)}
                                                     style = {{display: 'flex', flexDirection: 'column'}}>
                                                        <p style={{fontSize: '17px', padding: '8px', color: '#1f1f1f'}}><b>{problems.weak_tag_problems[selectedField_weak].explainations[index][1]}</b></p>
                                                        <p style={{fontSize: '3px'}}><br></br></p>
                                                        <p >난이도: {problems.weak_tag_problems[selectedField_weak].explainations[index][2]}</p>
                                                        <p>평균 시도 횟수: {problems.weak_tag_problems[selectedField_weak].explainations[index][3]}</p>
                                                        </button>
                                                </div>
                                                ))}
                                                </div>
                                            </div>
                                )}
                                <div style={{ textAlign: 'right', paddingRight: '3%' }}>
                                    <path d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"></path>
                                    <p data-tip = {`취약 유형은 ${problems.user_id}님의 해당 유형의 정답률, 푼 문제 수 등을 고려하여 산출돼요.`}
                                        className = 'qmark'>
                                        취약 유형이란?</p>
                                    <ReactTooltip place="left" type="dark" effect="solid"/>
                                </div>

                            </div>
                    </>
                    )}
                    {currentPage === 2 && (
                        <>
                        <div style={{fontSize: '23px', fontFamily: 'Arial, sans-serif', marginBottom: '2px', textAlign: 'center', marginTop: '13px', color: '#202125'}}>
                            해당 분류의 문제를 푼 지 오래됐어요.
                        </div>
                        <p style={{textAlign: 'center', marginBottom: '0px', color: '#5f6368'}}>나중엔 더 기억나지 않을 거예요!</p>
                        <div className="option-button-container">
                            <div style={{display: 'flex', alignItems: 'center'}}>   
                                <button className='reloadingM' onClick={() => handleRotate()}></button>  
                                <div className="option-button-container">   
                                    <button className="toggleOptions" onClick={toggleOptions} > 난이도 필터 </button>
                                    <CSSTransition
                                        in={isOptionsVisible}
                                        timeout={250}
                                        classNames="options"
                                        unmountOnExit
                                    >
                                        <div className="options">
                                            <button onClick={() => handleFilter('None')}>무작위</button>
                                            <button onClick={() => handleFilter('Silver')}>실버</button>
                                            <button onClick={() => handleFilter('Gold')}>골드</button>
                                            <button onClick={() => handleFilter('Platinum')}>플래티넘</button>
                                            <button onClick={() => handleFilter('Diamond')}>다이아몬드</button>
                                        </div>
                                    </CSSTransition>
                                </div>
                            </div>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                            <div className='divStyle'>
                                <div className='Box' id = 'Box1'>
                                    <div className = 'pBox' id = "Problem1">
                                        <a 
                                        data-tip = {`난이도: ${problems.forgotten_tag_problems.tag1.problem.level}, 분류: ${problems.forgotten_tag_problems.tag1.tag}`}
                                        className = 'hrefBox' href={`https://www.acmicpc.net/problem/${problems.forgotten_tag_problems.tag1.problem.problemID}`}>
                                             {problems.forgotten_tag_problems.tag1.problem.titleKo} </a>
                                    </div>
                                    <div className = 'eBox' id = "explanation1">
                                        현재 {problems.forgotten_tag_problems.tag1.tag} 내용을 {problems.forgotten_tag_problems.tag1.forgottenPercent}% 기억하고 있어요.   
                                    </div>
                                </div>
                                <div className='Box' id = 'Box2'>
                                    <div className = 'pBox' id = "Problem2">
                                        <a 
                                        className = 'hrefBox' href={`https://www.acmicpc.net/problem/${problems.forgotten_tag_problems.tag2.problem.problemID}`}
                                        data-tip = {`난이도: ${problems.forgotten_tag_problems.tag2.problem.level}, 분류: ${problems.forgotten_tag_problems.tag2.tag}`}
                                        >
                                         {problems.forgotten_tag_problems.tag2.problem.titleKo} </a>
                                    </div>
                                    <div className = 'eBox' id = "explanation2">
                                    현재 {problems.forgotten_tag_problems.tag2.tag} 내용을 {problems.forgotten_tag_problems.tag2.forgottenPercent}% 기억하고 있어요.   
                                    </div>
                                </div>
                                <div className='Box' id = 'Box3'>
                                    <div className = 'pBox' id = "Problem3">
                                        <a 
                                            data-tip = {`난이도: ${problems.forgotten_tag_problems.tag3.problem.level}, 분류: ${problems.forgotten_tag_problems.tag3.tag}`}
                                            className = 'hrefBox'
                                            href={`https://www.acmicpc.net/problem/${problems.forgotten_tag_problems.tag3.problem.problemID}`}>
                                             {problems.forgotten_tag_problems.tag3.problem.titleKo} </a>
                                    </div>
                                    <div className = 'eBox' id = "explanation3">
                                    현재 {problems.forgotten_tag_problems.tag3.tag} 내용을 {problems.forgotten_tag_problems.tag3.forgottenPercent}% 기억하고 있어요.   
                                    </div>
                                </div>
                            </div>
                            <div style={{ textAlign: 'right', fontSize: '13px', paddingRight: '3%', height: '33px'}}>
                                 <a 
                                 data-tip = {`해당 문제들은 독일의 심리학자 헤르만 에빙하우스의 망각곡선에 기반하여 ${problems.user_id}님이 오래 동안 풀지 않은 유형의 문제를 추천해 드리고 있어요.`}
                                 style={{color: 'black', fontWeight: 'bold'}} href='https://ko.wikipedia.org/wiki/%EB%A7%9D%EA%B0%81_%EA%B3%A1%EC%84%A0'>
                                    에빙하우스의 망각곡선</a>
                            </div>
                            <ReactTooltip place="top" type="dark" effect="solid"/>
                        </div>
                        </>
                    )}
                    {currentPage === 3 && (
                        <>
                        <div style={{fontSize: '24px', fontFamily: 'Arial, sans-serif', textAlign: 'center', marginTop: '13px', color: '#202125'}}>
                                이런 문제는 어떤가요?
                        </div>
                        <p style={{textAlign: 'center', marginBottom: '0px', color: '#5f6368'}}>{problems.user_id}님과 비슷한 실력의 유저들이 많이 푼 문제들을 가져왔어요!</p>
                        <div style={{display: 'flex', alignItems: 'center'}}>   
                            <button className='reloadingM' onClick={() => handleRotate()}></button>  
                            <div className="option-button-container">   
                                <button className="toggleOptions" onClick={toggleOptions} > 난이도 필터 </button>
                                <CSSTransition
                                    in={isOptionsVisible}
                                    timeout={250}
                                    classNames="options"
                                    unmountOnExit
                                >
                                    <div className="options">
                                        <button onClick={() => handleFilter('None')}>무작위</button>
                                        <button onClick={() => handleFilter('Silver')}>실버</button>
                                        <button onClick={() => handleFilter('Gold')}>골드</button>
                                        <button onClick={() => handleFilter('Platinum')}>플래티넘</button>
                                        <button onClick={() => handleFilter('Diamond')}>다이아몬드</button>
                                    </div>
                                </CSSTransition>
                            </div>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                        
                            <div className='divStyle'>
                                <div className='Box' id = 'Box1'>
                                    <div className = 'pBox' id = "Problem1">
                                        <a 
                                        data-tip = {`난이도: ${problems.similarity_based_problems.problem1.level}, 분류: ${problems.similarity_based_problems.problem1.tags}`}
                                        className = 'hrefBox'
                                        href = {`https://www.acmicpc.net/problem/${problems.similarity_based_problems.problem1.problemID}`}>
                                            {problems.similarity_based_problems.problem1.titleKo}
                                        </a>
                                    </div>
                                    <div className = 'eBox' id = "explanation1" style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                                        <p>난이도: {problems.similarity_based_problems.problem1.level}</p>
                                        <p>평균 시도 횟수: {problems.similarity_based_problems.problem1.averageTries}</p>
                                        <p>분류: {problems.similarity_based_problems.problem1.tags}</p>
                                    </div>
                                </div>
                                <div className='Box' id = 'Box2'>
                                    <div className = 'pBox' id = "Problem2">
                                        <a 
                                        data-tip = {`난이도: ${problems.similarity_based_problems.problem2.level}, 분류: ${problems.similarity_based_problems.problem2.tags}`}
                                        className = 'hrefBox'
                                        href={`https://www.acmicpc.net/problem/${problems.similarity_based_problems.problem2.problemID}`}>
                                            {problems.similarity_based_problems.problem2.titleKo}</a>
                                    </div>
                                    <div className = 'eBox' id = "explanation2" style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                                        <p>난이도: {problems.similarity_based_problems.problem2.level}</p>
                                        <p>평균 시도 횟수: {problems.similarity_based_problems.problem2.averageTries}</p>
                                        <p>분류: {problems.similarity_based_problems.problem2.tags}</p>
                                    </div>
                                </div>
                                <div className='Box' id = 'Box3'>
                                    <div className = 'pBox' id = "Problem3">
                                        <a 
                                            data-tip = {`난이도: ${problems.similarity_based_problems.problem3.level}, 분류: ${problems.similarity_based_problems.problem3.tags}`}
                                            className = 'hrefBox'
                                            href = {`https://www.acmicpc.net/problem/${problems.similarity_based_problems.problem3.problemID}`}>
                                                {problems.similarity_based_problems.problem3.titleKo}</a>
                                    </div>
                                    <div className = 'eBox' id = "explanation3" style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                                        <p>난이도: {problems.similarity_based_problems.problem3.level}</p>
                                        <p>평균 시도 횟수: {problems.similarity_based_problems.problem3.averageTries}</p>
                                        <p>분류: {problems.similarity_based_problems.problem3.tags}</p>
                                    </div>
                                </div>
                            </div>
                                <ReactTooltip place="top" type="dark" effect="solid"/>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

interface MyPageRequest {
    url: string;
    div: number;
    filter: string;
  }  

interface Problem {
    problemID: string;
    titleKo: string;
    level: string;
    averageTries: number;
    tags: string[];
  }
  
  interface Explaination {
    problemID: string;
    titleKo: string;
    level: string;
    averageTries: number;
  }

  interface Tag {
    tag_name: string;
    problems: string[];
    explainations: Explaination[];
    weak_pcr: number;
  }
  
  interface WeakTagProblems {
    [key: string]: Tag;
  }
  
  interface ForgottenTagProblems {
    [key: string]: {
      tag: string;
      forgottenPercent: number;
      problem: Problem;
    };
  }
  
  interface SimilarityBasedProblems {
    problem1: Problem;
    problem2: Problem;
    problem3: Problem;
  }
  
  interface ResponseData {
    user_id: string;
    weak_tag_problems: WeakTagProblems;
    forgotten_tag_problems: ForgottenTagProblems;
    similarity_based_problems: SimilarityBasedProblems;
  }
  
export default MyPage;
