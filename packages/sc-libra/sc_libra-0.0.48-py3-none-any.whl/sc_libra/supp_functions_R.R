#Test function
filtered <- function(df, valor1, valor2){
  df = df[valor1:valor2,valor1:valor2]
  return(df)
}

#Bimodal distances obtain function
biomodal_distances <- function(distance_matrix){
  distance_vector = distance_matrix[,1]
  bimodal_1_all = c()
  bimodal_2_all = c()
  bimodal_1_mean_all = c()
  bimodal_1_mean_all = c()
  bimodal_1_mean_all = c()
  bimodal_2_mean_all = c()
  bimodal_2_mean_all = c()
  bimodal_2_mean_all = c()
  bimodal_1_mean = c()
  bimodal_1_median = c()
  bimodal_1_sd = c()
  bimodal_2_mean = c()
  bimodal_2_median = c()
  bimodal_2_sd = c()
  #Start
  d <- density(distance_vector)
  minimun_local = optimize(approxfun(d$x,d$y),interval=c(((min(distance_vector)*125)/100),((max(distance_vector)*60)/100)))$minimum
  #Min distance
  min_distance = min(distance_vector)
  modal_1 = distance_vector[distance_vector < minimun_local & distance_vector > min_distance]
  
  #Max distance
  max_distance = max(distance_vector)
  modal_2 = distance_vector[distance_vector > minimun_local & distance_vector < max_distance]
  
  mean_range = (abs(min_distance - minimun_local) / 4)

  #modal_1
  h = hist(modal_1, breaks=100000)
  i = which.max(h$counts)
  max_peak_modal_1 = h$mids[i]

  peak_upper = max_peak_modal_1 + mean_range
  peak_botton = max_peak_modal_1 - mean_range
  
  if (peak_upper < max(modal_1)) {
    peak_upper = peak_upper
  } else {
    peak_upper = max(modal_1)
  }
  if (peak_botton > min(modal_1)) {
    peak_botton = peak_botton
  } else {
    peak_botton = min(modal_1)
  }   
  
  modal_1_peak_zone = modal_1[(modal_1 > peak_botton) & (modal_1 < peak_upper)]
  
  bimodal_1_mean = append(bimodal_1_mean, mean(modal_1_peak_zone))
  bimodal_1_median = append(bimodal_1_median, median(modal_1_peak_zone))
  bimodal_1_sd = append(bimodal_1_sd, sd(modal_1_peak_zone))
  
  #modal_2
  h = hist(modal_2, breaks=100000)
  i = which.max(h$counts)
  max_peak_modal_2 = h$mids[i]

  peak_upper = max_peak_modal_2 + mean_range
  peak_botton = max_peak_modal_2 - mean_range
  
  if (peak_upper < max(modal_2)) {
    peak_upper = peak_upper
  } else {
    peak_upper = max(modal_2)
  }
  if (peak_botton > min(modal_2)) {
    peak_botton = peak_botton
  } else {
    peak_botton = min(modal_2)
  }   
  
  modal_2_peak_zone = modal_2[(modal_2 > peak_botton) & (modal_2 < peak_upper)]
  
  bimodal_2_mean = append(bimodal_2_mean, mean(modal_2_peak_zone))
  bimodal_2_median = append(bimodal_2_median, median(modal_2_peak_zone))
  bimodal_2_sd = append(bimodal_2_sd, sd(modal_2_peak_zone)) 

  bimodal_1_mean_all = mean(bimodal_1_mean)
  bimodal_1_median_all = mean(bimodal_1_median)
  bimodal_1_sd_all = mean(bimodal_1_sd)
    
  bimodal_2_mean_all = mean(bimodal_2_mean)
  bimodal_2_median_all = mean(bimodal_2_median)
  bimodal_2_sd_all = mean(bimodal_2_sd)
    
  bimodal_1_all = append(bimodal_1_all, bimodal_1_mean_all)
  bimodal_1_all = append(bimodal_1_all, bimodal_1_median_all)
  bimodal_1_all = append(bimodal_1_all, bimodal_1_sd_all)
  print(bimodal_1_all)
    
  bimodal_2_all = append(bimodal_2_all, bimodal_2_mean_all)
  bimodal_2_all = append(bimodal_2_all, bimodal_2_median_all)
  bimodal_2_all = append(bimodal_2_all, bimodal_2_sd_all)
  print(bimodal_2_all)
  
  output_matrix = data.frame(bimodal_1_all, bimodal_2_all)
  
  return(output_matrix)
}

#supp_function
JaccardSets<- function(set1, set2){
        length(intersect(set1, set2))/length(unique(c(set1, set2)))
}

PairWiseJaccardSets<- function(ident1, ident2){
      ident1.list<- split(names(ident1), ident1)
      ident2.list<- split(names(ident2), ident2)
      res<- matrix(nrow = length(ident1.list), ncol = length(ident2.list),
                   dimnames = list(names(ident1.list), names(ident2.list)))
      for (i in seq_along(ident1.list)){
              res[i, ]<- purrr::map_dbl(ident2.list, ~JaccardSets(ident1.list[[i]], .x))
      }
      return(res)
}

PairWiseJaccardSetsHeatmap = function(ident1, ident2, best_match = FALSE,
                                      title = NULL, col_low = "white", col_high= "red",
                                      cluster_rows = F, cluster_columns =F,
                                      show_row_dend = F, show_column_dend = F, ...){
        cell_fun = function(j, i, x, y, width, height, fill) {
                grid::grid.rect(x = x, y = y, width = width *0.99, height = height *0.99,
                          gp = grid::gpar(col = "grey", fill = fill, lty = 1, lwd = 0.5))
        }
        mat<- PairWiseJaccardSets(ident1, ident2)
        col_fun<- circlize::colorRamp2(c(0, 1), c(col_low, col_high))
        if (best_match){
                cluster_rows = F
                cluster_columns =F
                show_row_dend = F
                show_column_dend = F
                match_idx<- MatchClusters(ident1, ident2)
                ComplexHeatmap::Heatmap(mat[, match_idx$ident2],
                                        cluster_rows = cluster_rows, cluster_columns = cluster_columns,
                                        show_row_names = T, show_column_names = T,
                                        show_row_dend = show_row_dend,
                                        show_column_dend = show_column_dend,
                                        col = col_fun, rect_gp = grid::gpar(type = "none"),
                                        cell_fun = cell_fun,
                                        name = "Jaccard index",
                                        column_title = title,
                                        heatmap_legend_param = list(color_bar = "discrete"),
                                        ...)
        }
        else{
                ComplexHeatmap::Heatmap(mat,
                                        cluster_rows = cluster_rows, cluster_columns = cluster_columns,
                                        show_row_names = T, show_column_names = T,
                                        show_row_dend = show_row_dend,
                                        show_column_dend = show_column_dend,
                                        col = col_fun, rect_gp = grid::gpar(type = "none"),
                                        cell_fun = cell_fun,
                                        name = "Jaccard index",
                                        column_title = title,
                                        heatmap_legend_param = list(color_bar = "discrete"),
                                        ...)

        }

}

#PPJI compute function
ppji <- function(latent,origin,the_name){
  #library(scclusteval, include.only = 'PairWiseJaccardSetsHeatmap')
  #library(scclusteval)
  jacard_vector_score = c()
  jacard=PairWiseJaccardSetsHeatmap(origin, latent,
                         show_row_dend = F, show_column_dend = F,
                         cluster_row = F, cluster_column =F)
  the_name
  pdf(file=paste0(the_name,"_ppji_heatmap.pdf"), width=12, height=6)
    print(jacard)
  dev.off()
  jacard_distance = jacard@matrix
  is.na(jacard_distance) <- jacard_distance==0
  jacard_distance = jacard_distance[,colSums(is.na(jacard_distance))<nrow(jacard_distance)]
  jacard_vector_score = append(jacard_vector_score, mean(apply(jacard_distance,1,sum, na.rm=TRUE)))
  print(jacard_vector_score)
  return(jacard_vector_score)
}