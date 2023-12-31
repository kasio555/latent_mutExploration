from typing import Dict, Tuple, Union
from mutants.abstract_mutant import AbstractMutantCont

class PitMutantCont(AbstractMutantCont):
    def __init__(self, 
        mutNo:int, 
        left:Dict, 
        right:Dict, 
        mutOp:str,
        targeted,
        mutated_fpath:str, # the original starting point 
        # 
        pos:Tuple[int, int, int], 
        mut_target_text:Union[str, Tuple], 
    ):
        super().__init__(
            mutNo, 
            left, 
            right, 
            mutOp, 
            targeted,  
            mutated_fpath
        )
        self.target_node = targeted 
        if isinstance(mut_target_text, Tuple): # meaning the targed org_text of the element was negative 
            self.neg_prefix, self.mut_target_text = mut_target_text
        else:
            self.mut_target_text = mut_target_text
            self.neg_prefix = None
        self.start, self.end = pos[0], pos[0] # line number
        self.start_chr_cnt, self.end_chr_cnt = pos[1:]
        self.start_chr_loc = self.start_chr_cnt - 1 # originally position, now index
        self.end_chr_loc = self.end_chr_cnt #
        self.appliedAts = {
            self.mutated_fpath:[
                [self.mut_target_text,
                (self.start_chr_loc, self.end_chr_loc)]
            ]
        } 
        self.tempApplyAts = {} 
    
    def getContentToReplace(self) -> str:
        return self.right

    def applyMutation(
        self, 
        newloc:Tuple[int, int], 
        targetContent:str, 
    ) -> str: 
        """
        """
        start, end = newloc
        _content = self.getContentToReplace()
        ## the negative prefix will be handled by there
        if self.neg_prefix is None:
            mutatedContent = targetContent[:start] + _content + targetContent[end:]
        else:
            idx_to_prefix = start - 1 
            cnt_whitespace = 0
            for i,c in enumerate(targetContent[:start][::-1]): 
                if not bool(c.strip()): 
                    cnt_whitespace += 1 
                else: # first met 
                    break 
            idx_to_prefix -= cnt_whitespace
            _prefix = targetContent[idx_to_prefix]
            if _prefix != '-':
                return None # the targeted one has been changed
            else:
                mutatedContent = targetContent[:idx_to_prefix] + _content + targetContent[end:]
        return mutatedContent
