import axios from 'axios'

export const getData = async (
    url: string,
    numProblems: number,
    rotate: number,
    filterTier: string
): Promise<ResponseData|null> => {
    try {
      // https://recproblem.site
      const response = await axios.post(
          'http://127.0.0.1:8000/mypage/problems',
          {
              url,
              numProblems: numProblems,
              div: rotate,
              filter: filterTier,
          },
          {
              headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (response) {
            console.log(response)
            return response.data;
        }
        return null
    }
    catch (error) {
      console.error('에러 발생:', error);
      return null
    }
}

export type Problem = {
    problemID: string;
    titleKo: string;
    level: string;
    averageTries: number;
    tags: string; // 문자열 배열에서 단일 문자열로 변경
}

export type Explaination = {
    problemID: string;
    titleKo: string;
    level: string;
    averageTries: number;
    tags: string; // 서버 모델에 맞춰 tags 필드 추가
}

export type WeakTagProblem = {
    tag_name: string;
    problems: string[];
    explainations: Explaination[];
    weak_pcr: number;
}

export type ForgottenTagProblem = {
    tag: string;
    forgottenPercent: number;
    problem: Problem;
}

export type ResponseData = {
    user_id: string;
    weak_tag_problems: WeakTagProblem[];
    forgotten_tag_problems: ForgottenTagProblem[];
    similarity_based_problems: Problem[];
}
