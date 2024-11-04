import type { ResponseExpItem, GroupedExpItem } from '@/types/exp';

export const preProcessDetail = (data: ResponseExpItem[]): GroupedExpItem[] => {
  const processData: { [key: string]: GroupedExpItem } = {};

  data.forEach(item => {
    // 불필요한 숫자 삭제
    const lv2ExpNm = item.lv2_exp_nm.replace(/^\d+\.\d+\./, '');

    if (!processData[lv2ExpNm]) {
      processData[lv2ExpNm] = {
        lv2_exp_nm: lv2ExpNm,
        lv3_exp_nm: []
      };
    }

    processData[lv2ExpNm].lv3_exp_nm.push(item.exp_nm);
  });

  return Object.values(processData);
};
