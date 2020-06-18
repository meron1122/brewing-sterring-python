import {Component, OnInit, TemplateRef} from '@angular/core';
import {RecipesService} from "../../shared/api/recipes.service";
import {IRecipe} from "../../shared/models/irecipe";
import {BsModalRef, BsModalService} from "ngx-bootstrap/modal";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-recipes-list',
  templateUrl: './recipes-list.component.html',
  styleUrls: ['./recipes-list.component.css']
})
export class RecipesListComponent implements OnInit {

  recipes: Partial<IRecipe[]>;
  modalRef: BsModalRef;
  tempRecipe: Partial<IRecipe>;

  constructor(public recipesApi: RecipesService, private modalService: BsModalService, private toastr: ToastrService) {
  }

  ngOnInit(): void {
    this.refreshList();
  }

  private refreshList() {
    this.recipesApi.getRecipes$().subscribe((value => this.recipes = value));
  }

  openModal(template: TemplateRef<any>) {
    this.tempRecipe = {};
    this.modalRef = this.modalService.show(template);
  }

  createRecipe() {
    this.recipesApi.createRecipe$({name: this.tempRecipe.name, id: null}).subscribe(() => {
        this.tempRecipe = null;
        this.modalRef.hide();
        this.refreshList();
        this.toastr.success('Dodano recepturę!');
      }, () => this.toastr.error('Wystąpił błąd podczas zapisu!')
    )
  }

  deleteRecipe(id: number) {
    this.recipesApi.deleteRecipe$(id).subscribe(() => {
        this.refreshList();
        this.toastr.success('Usunięto recepturę!');
      }, () => this.toastr.error('Wystąpił błąd podczas usuwania!')
    )
  }
}
