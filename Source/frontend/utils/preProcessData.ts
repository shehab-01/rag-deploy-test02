import type { ExpItem, ResponseExpItem } from '@/types/exp';

export const preprocessData = (data: ResponseExpItem[]): ExpItem[] => {
  let processedData: ExpItem[] = [];
  let lastLv1ExpNm = '';
  let lastLv2ExpNm = '';
  data.forEach(item => {
    let newItem: ExpItem = {
      lv1_exp_nm: item.lv1_exp_nm,
      lv2_exp_nm: `${item.lv2_exp_nm} (${item.hi_exp_id})`,
      exp_nm: item.exp_nm,
      exp_id: item.exp_id
    };

    if (item.lv1_exp_nm === lastLv1ExpNm) {
      newItem.lv1_exp_nm = '';
    } else {
      lastLv1ExpNm = item.lv1_exp_nm;
    }

    if (item.lv2_exp_nm === lastLv2ExpNm) {
      newItem.lv2_exp_nm = '';
    } else {
      lastLv2ExpNm = item.lv2_exp_nm;
    }

    processedData.push(newItem);
  });
  return processedData;
};
