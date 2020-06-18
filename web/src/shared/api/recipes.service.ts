import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { IRecipe } from '../models/irecipe';



@Injectable()
export class RecipesService  {

  protected apiUrl = 'http://localhost:5000/';

  constructor(protected http: HttpClient) {
  }

  getRecipes$(): Observable<IRecipe[]> {
    return this.http.get<IRecipe[]>(this.apiUrl + `recipes`);
  }

  createRecipe$(recipe: IRecipe): Observable<IRecipe> {
    return this.http.post<IRecipe>(this.apiUrl + 'recipes', recipe);
  }

  deleteRecipe$(id: number): Observable<any> {
    return this.http.delete<any>(this.apiUrl + 'recipes/'+ id);
  }

}
