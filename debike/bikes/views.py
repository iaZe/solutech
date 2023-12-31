from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from marketplace.models import Anuncio
from .forms import CadastrarBikeForm, ConsultarBikeForm, VenderBikeForm
from .models import Bike
from .utils import consultar_restricao, realizar_venda


@login_required
def cadastrar(request):
    if request.method == "POST":
        form = CadastrarBikeForm(request.POST, request.FILES)
        if form.is_valid():
            bike = form.save(commit=False)
            bike.dono = request.user
            bike.save()
            return redirect(reverse("inicio"))
    else:
        form = CadastrarBikeForm()
    return render(request, "cadastrar.html", {"form": form})


def consultar(request):
    if request.method == "POST":
        form = ConsultarBikeForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data["codigo"]
            restricao = consultar_restricao(request, codigo)
        return render(request, "consultar.html", {"form": form, "restricao": restricao})
    else:
        form = ConsultarBikeForm()
    return render(request, "consultar.html", {"form": form})

@login_required
def vender(request, codigo):
    bike = Bike.objects.filter(ID=codigo).first()
    if request.user != bike.dono:
        error = messages.error(request, "Bike não pertence ao usuário")
        return render(
            request, "consultar.html", {"form": ConsultarBikeForm(), "error": error}
        )
    if not bike:
        error = messages.error(request, "Bike não cadastrada")
        return render(
            request, "consultar.html", {"form": ConsultarBikeForm(), "error": error}
        )
    if bike.restricao:
        restricao = messages.warning(request, "Bike com restrição de roubo/furto")
        return render(
            request,
            "consultar.html",
            {"form": ConsultarBikeForm(), "restricao": restricao},
        )
    if request.method == "POST":
        form = VenderBikeForm(request.POST)
        if form.is_valid():
            realizar_venda(request, bike, form)
            if bike in Anuncio.objects.all():
                Anuncio.objects.filter(bike=bike).delete()
            return redirect(reverse("inicio"))
    else:
        form = VenderBikeForm()
    return render(request, "vender.html", {"form": form, "bike": bike})

@login_required
def restringir(request, codigo):
    bike = Bike.objects.filter(ID=codigo).first()
    print(bike)
    if request.user != bike.dono:
        error = messages.error(request, "Bike não pertence ao usuário")
        return render(
            request, "consultar.html", {"form": ConsultarBikeForm(), "error": error}
        )
    if not bike:
        error = messages.error(request, "Bike não cadastrada")
        return render(
            request, "consultar.html", {"form": ConsultarBikeForm(), "error": error}
        )
    if bike.restricao == True:
        bike.restricao = False
        messages.success(request, "Bike liberada com sucesso")
    else:
        bike.restricao = True
        messages.success(request, "Bike restringida com sucesso")
    bike.save()
    return redirect(reverse("inicio"))

@login_required
def excluir(request, codigo):
    bike = Bike.objects.filter(ID=codigo).first()
    if request.user != bike.dono:
        error = messages.error(request, "Bike não pertence ao usuário")
        return render(
            request, "consultar.html", {"form": ConsultarBikeForm(), "error": error}
        )
    if not bike:
        error = messages.error(request, "Bike não cadastrada")
        return render(
            request, "consultar.html", {"form": ConsultarBikeForm(), "error": error}
        )
    bike.delete()
    messages.success(request, "Bike excluída com sucesso")
    return redirect(reverse("inicio"))