import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

class Histogram_Matching(nn.Module):
    def __init__(self, differentiable=False):
        super(Histogram_Matching, self).__init__()
        self.differentiable = differentiable

    def forward(self, dst, ref):
        # B C
        B, C, H, W = dst.size()
        # assertion
        assert dst.device == ref.device
        # [B*C 256]
        hist_dst = self.cal_hist(dst)
        hist_ref = self.cal_hist(ref)
        # [B*C 256]
        tables = self.cal_trans(hist_dst, hist_ref)
        # [B C H W]
        rst = dst.clone()
        for b in range(B):
            for c in range(C):
                rst[b,c] = tables[b*c, (dst[b,c] * 255).long()]
        # [B C H W]
        rst /= 255.
        return rst
        
    def cal_hist(self, img):
        B, C, H, W = img.size()
        # [B*C 256]
        if self.differentiable: 
            hists = self.soft_histc_batch(img * 255, bins=256, min=0, max=255, sigma=3*25)
        else:
            hists = torch.stack([torch.histc(img[b,c] * 255, bins=256, min=0, max=255) for b in range(B) for c in range(C)])
        hists = hists.float()
        hists = F.normalize(hists, p=1)
        # BC 256
        bc, n = hists.size()
        # [B*C 256 256]
        triu = torch.ones(bc, n, n, device=hists.device).triu()
        # [B*C 256]
        hists = torch.bmm(hists[:,None,:], triu)[:,0,:]
        return hists

    def cal_trans(self, hist_dst, hist_ref):
        # [B*C 256]
        table = torch.arange(256, device=hist_dst.device).repeat(len(hist_dst), 1)
        for bc in range(len(table)):
            i = j = 1
            while i < 256:
                if j >= 256:
                    table[bc, i] = 255
                    i += 1
                elif hist_dst[bc, i] >= hist_ref[bc, j - 1] and hist_dst[bc, i] <= hist_ref[bc, j]:
                    table[bc, i] = j
                    i += 1
                else:
                    j += 1
        table[:, 255] = 255
        return table

    def soft_histc_batch(self, x, bins=256, min=0, max=255, sigma=3*25):
        # B C H W
        B, C, H, W = x.size()
        # [B*C H*W]
        x = x.view(B*C, -1)
        # 1
        delta = float(max - min) / float(bins)
        # [256]
        centers = float(min) + delta * (torch.arange(bins, device=x.device).float() + 0.5)
        # [B*C 1 H*W]
        x = torch.unsqueeze(x, 1)
        # [B*C 256 1]
        centers = centers.unsqueeze(0).repeat(B*C, 1).unsqueeze(2)
        # [B*C 256 H*W]
        x = x - centers
        # [B*C 256 H*W]
        x = torch.sigmoid(sigma * (x + delta/2)) - torch.sigmoid(sigma * (x - delta/2))
        # [B*C 256]
        x = x.sum(dim=2)
        # [B*C 256]
        return x

